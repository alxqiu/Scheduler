#comment on the communication protocols, what kind of stuff should be included on the json file

#for this part, literally just work on the client side, NOTHING that should be done on the server side
#therefore, this should have the interface without any job_template class to make objects, 
#don't need to have any sort of object creation here for jobs
#research how to write the client script:
    #research "requests"", use "posts" and json, and pickle
        #pickle converts arguments into string, and trns into json
        #1: requests 2: pickle, 3: understand json

    #verify security headers in the server, thats more of a complex task
import requests
import pickle
import json
import urllib.parse
from threading import Event
from time import sleep
import base64

class Executor():
    #delete this __init__ when I've finished server side implementation
    def __init__(self, url, path = None, params = None):
        self.url_str = url
           
        #recode this section into taking host and port as params


    #condensed into the signature of the concurrent.futures.executor.submit() method, 
        ##new method signature:
            #submit(fn, *args, job_config, **kwargs):
        #########
    def submit(self, fn, *args, job_config = {}, **kwargs):
        #fn: denotes a function object: pickle it into a string. Doesn't store function itself, but its a fully qualified
        #name for the function. 
        fn = str(base64.b64encode(pickle.dumps(fn)).decode('utf-8'))
        args = str(base64.b64encode(pickle.dumps(args)).decode('utf-8'))
        kwargs = str(base64.b64encode(pickle.dumps(kwargs)).decode('utf-8'))
            # pickle all the args and then unpickle on the server side, just don't pickle job_config. 
        data  = {'fn': fn, 'func_args': args, 'func_kwargs': kwargs}
            #the submitted callable "fn" should be executed as fn(*args, **kwargs)
        default_config = {'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
        if len(job_config.keys()) is not 0:
            assert set(job_config.keys()) < set(default_config.keys())
            #this allows the new, explicitly defined values to override defaults.      
            default_config.update(job_config)
        #If job_config is explicitly defined, defined values won't be overwritten. 
        data.update(default_config)
        r = requests.post(self.url_str + '/submit-request', json = data)  
            #only sends back {'job_id': <job_id>}
        assert r.status_code == 200
        job_id = r.json().get('job_id')
        assert job_id is not None
        new_future = Future(fn, job_id, self.url_str, args, kwargs)
        return new_future  

    #debugging functions to view the serverside instance variables
    def get_data_for_jobs(self):
        r = requests.get(url = self.url_str + '/get-data-for-jobs')
        return r.text
    def get_runnable_jobs(self):
        r = requests.get(url = self.url_str + '/get-runnable-jobs')
        return r.text

    #INTERNAL FUNCTION: grab info from server
        #memory, priority, retries, running, success, exception
        #minimal info in the query payload that is sent over, just wanted to have something
        #for the server to know that there is a request to GET info
            ###prevent this from being accessible later...
    #needs to be accessed through job_id
    def _grab(self, job_id):
        r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': job_id})
        assert r.status_code != 404
        assert r.json() is not None
        return r.json()
       
    #rewrite this to be based on future objects
    def shutdown(self, wait = True):
        if wait:
            while wait:
               # need to write a request that can cover the futures that the interface has access to?
                if (r['running'] == True):
                    wait = False

        #if done waiting, or if not waiting, send a post to shut down operations
        r = requests.post(url = self.url_str + '/kill')
        print('shut down achieved')
            

#future doesn't need much aside from a means to identify a job and the way to contact it in the server
#when you read result, if its not completed it would just be blocked, as the job is still running
class Future():
    def __init__(self, fn, job_id, url_str, *args, **kwargs):
       self.fn = fn
       self.job_id = job_id
       self.url_str = url_str
       self.func_args = args
       self.func_kwargs = kwargs
    def future_info(self):
        info_dict = {
            'fn': self.fn, 
            'job_id': self.job_id, 
            'url_str': self.url_str, 
        }
        return info_dict
        
    def cancel(self):
        #won't even attempt to cancel if it is running or already cancelled
        if running() or cancelled():
            #returns false if it is currently running or already cancelled
            return False
        else: 
            r = requests.post(self.url_str + '/cancel-job', json = {'job_id': self.job_id})
            #change this so that it can have info to cancel a job, and have it specific for a job_id
            return True

    def cancelled(self):
        r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id})
        return r.json()['cancelled']

    #distinct from the done method as this works whether started or not
    def running(self):
        #make sure you check to see if it was started, DO NOT depend on done()
         r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id})
         return r.json()['running']

    def done(self):
         r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id})
         if (r.json()['cancelled'] or r.json()['complete']):
             return True
         else:
             return False

    #can't do regular "done" thing, needs to 
        #raise CancelledError
        #and also mirror the exception raised by the call
    def result(self, timeout = None):
        if (timeout is None): 
            timeout = 1.0
        time_check = True
        return_value = None
        timer = 0.0
        result = None
        while (time_check):
            sleep(1.0)
            timer += 1.0
            r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id}).json()
            if (r['cancelled'] == True):
                raise CancelledError
            if (r['exception'] is not None):
                #develop system to have the same exceptions
                raise r['exception']
            if (r['complete'] == True):
                result = r['result']
                break
            if (timer > timeout):
                raise TimeoutError  
        return result

    #we are talking about the exceptions in the job itself
    def exception(self, timeout = None):
        if (timeout is None): 
            timeout = 1.0
        time_check = True
        return_value = None
        timer = 0.0
        while (time_check):
            sleep(1.0)
            timer += 1.0
            r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id}).json()
            if (r['cancelled'] == True):
                raise CancelledError
            if (r['complete'] == True):
                break
            if (timer > timeout):
                raise TimeoutError
        #per project parameters, this will return default value of r['exception']
            #which is None
        return r['exception']

    #this just runs a function directly after the completion of the job
    #can assume these functions are only going to reference the job info itself, 
        #as they take the future object as the only parameter
        #they can be as simple as printing the results of the job
    def add_done_callback(self, fn):
        waiting = True
        while (waiting):
            sleep(1.0)
            r = requests.get(url = self.url_str + '/grab-job-info', json = {'job_id': self.job_id})
            if (r.json['cancelled'] or r.json['complete']):
                break
        #says that the callable fn should run with "future" as it's only argument
        fn(self)

    class TimeoutError(Exception):
        #raise when there is a timeout on the results method for futures.
        pass
    class CancelledError(Exception):
        pass



