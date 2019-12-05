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
        default_config = {'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
        if job_config is not None:
            for ky in job_config.keys():
                assert (ky in ('memory', 'priority', 'retries', 'run_now'))
            #adds default vals to missing vals, after checking for validity
            default_config.update(job_config)

        #if input is none, the thing gets updated w default vals
        job_config.update(default_config)
        data.update(job_config)
        r = requests.post(self.url_str, json = data)    
        assert r.json() is not None
        #define here what the server should return back to me
            #define acceptable values here, perhaps write documentation for the clear inputs/returns from the server.
            #perhaps assertions.
        new_future = Future(fn, self.url_str, job_config, args, kwargs)
        
        #return new_future
        return r

    #INTERNAL FUNCTION: grab info from server
        #memory, priority, retries, running, success, exception
    def _grab(self, fn, query_payload = {'memory': None, 'priority': None, 'retries': None, 
                                            'running': None, 'success': False, 'exception': None}):
        #params for the desired info to grab from the server
        query_payload.update({'fn': fn})
        r = request.get(url = self.url_str, json = query_payload)
            #information returned by server is defined by server side script.

        assert r.json() is not None
            #assert other elements here
        return r.json()
        
    def shutdown(self, wait = True):
        #grab server info and try to assess if job is done or not
        self.url_str

        #get result from Future.running() to see if the jobs can be shut down
        #don't need specific names, just check all available

        if wait:
            args = False
        return args
            

#this is all about the references to the actual job object, a means to reference from client
#the future object is responsible for getting inquiries from the client about the server
#and should keep all the info for the server and name, and facilitate communication between server and client
    #no need to predefine default vals for job_config, since that's already done in the submit method

class Future():
    def __init__(self, fn, url_str, job_config, *args, **kwargs):
       self.fn = fn
       self.url_str = url_str
       self.func_args = args
       self.func_kwargs = kwargs
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