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
import json
import urllib.parse

class Executor():
    #delete this __init__ when I've finished server side implementation
    def __init__(self, url, path = None, params = None):
        self.url_str = url
           
        #recode this section into taking host and port as params

        print(self.url_str)
    
    #condensed into the signature of the concurrent.futures.executor.submit() method, 
    #with additional params noted in a separate dict: job_config = 
    #       {'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
        ##new signature:
            #submit(fn, *args, job_config, **kwargs):
    def submit(self, fn, *args, job_config = {}, **kwargs):

        data  = {'fn': fn, 'func_args': args, 'func_kwargs': kwargs}
            #the submitted callable "fn" should be executed as fn(*args, **kwargs)
        default_config = {'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
        #if input is none, we send default values
        #check for elements present in job_config but not in default keys, then adding appropriate values to default
        if job_config is not None:
            assert len(set(job_config.keys()) - set(default_config.keys())) == 0
                #I would have used (if setA.difference(setB) is None), but difference returns 'set()'
                #and I don't know how to express that as a value to compare     
            default_config.update(job_config)
        data.update(default_config)

        r = requests.post(self.url_str + '/submitRequest', json = data)  
        #defs of acceptable returns
        assert r.status_code != 404
        assert r.json()['priority'] is not None
        assert r.json()['memory'] is not None
        assert r.json()['retries'] is not None
        assert r.json()['job_id'] is not None
            #this type of formatting works, reference data through r.json()
        print("r.text:\n\t" + r.text)
        job_id = r.json()['job_id']

        #make sure job_id can be saved in the future object
        new_future = Future(fn, job_id, self.url_str, args, kwargs)
        return new_future  
        
        
    #INTERNAL FUNCTION: grab info from server
        #memory, priority, retries, running, success, exception
        #minimal info in the query payload that is sent over, just wanted to have something
        #for the server to know that there is a request to GET info
            ###prevent this from being accessible later...
    #needs to be accessed through job_id
    def _grab(self, job_id):
        query_payload = {'job_id': job_id, '_grab': True}
        r = requests.get(url = self.url_str + '/handleGETRequest', json = query_payload)
        assert r.status_code != 404
        assert r.json() is not None
        return r.json()
       
    #how to make sure that this can work without needing to go job by job?
    #or is that necessary?
    def shutdown(self, wait = True):
        while wait:
            r = _grab(None)
            if (r['running'] == True):
                wait = False
        #at the end of waiting, send a post to shut down operations
        r = request.post(url = self.url_str, json = {'shutdown': True})

        #add in thing for r to have success attr for this part
        return r.success
            

#future doesn't need much aside from a means to identify a job and the way to contact it in the server
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
            'func_args': self.func_args, 
            'func_kwargs': self.func_kwargs
        }
        return info_dict
        
    def cancel(self):

        return False

    def cancelled(self):
        return ((self.running) == False)

    def running(self):
        r = requests.get(self.url_str)
        #grabs status of whether the job object is running or not
        return r.running

    def done(self):
        return True
    def result(self, timeout = None):
        success = False

        if success:
            return success
        else:
            return success
    def exception(self, timeout = None):
        #check for successful run without any exceptions

        return None
    def add_done_callback(self, fn):
        fn