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

    def submit(self, fn, job_name, memory, *args, priority = 1, retries = 0, run_now = False, **kwargs):
        #just as fn denotes the callable in futures, the submit(job_name....) should schedule the callable          
        data  = {'fn': fn, 'job_name': job_name, 'memory': memory, 'priority': priority, 
                 'retries': retries, 'run_now': run_now, 'func_args': args, 'func_kwargs': kwargs}
        ###
            #problem: based on the response of the server, the names of the args and kwargs can be returned but not the values
            #current syntax appears to be correct, that won't spawn runtime error
        ###
        r = requests.post(self.url_str, json = data)
            #check if the response takes the actual one:
            #define here what the server should return back to me
            #define acceptable values here, perhaps write documentation for the clear inputs/returns from the server.
            #perhaps assertions.    
        assert r.json() is not None
            #not sure what this would look like for a lot of other urls though...
            #so not sure what to check for.  

        new_future = Future(fn, self.url_str, memory, priority, retries, args, kwargs)
        #the object doesn't have the job specifications itself, function_name should be the path
       
        #return new_future
        return r

    #next I want to include a function that will grab info from the server
    #   we want:
        #memory, priority, retries, running, success, exception

    def grab(self, fn, job_name):
        #params for the desired info to grab from the server
        payload = {'fn':fn, 'job name': job_name, 'memory': None,  'priority': None, 
                   'retries': None, 'running': None, 'query': True, 'success': False, 'exception': None} 
            #do not need to get information from the job specific args and kwargs
        r = request.get(url = self.url_str, params = payload)
            #information returned by server is defined by server side script.

        assert r.json() is not None
            #assert other elements here
        return r.json()
        
    def shutdown(self, wait = True):
        #grab server info and try to assess if job is done or not
        self.server_info

        args = True
        #get result from Future.running() to see if the jobs can be shut down
        #don't need specific names, just check all available

        if wait:
            args = False
        return args
            

#this is all about the references to the actual job object, a means to reference from client
#the future object is responsible for getting inquiries from the client about the server
#and should keep all the info for the server and name, and facilitate communication between server and client
class Future():
    def __init__(self, function_name, server_info, memory, priority, retries, *args, **kwargs):
       self.job_name = function_name
       #self.server_info = server_info
       #assert ((self.server_info[0] is not None) and (self.server_info[1] is not None))
       #self.url_str = "http://" + self.server_info[0] + ":" + self.server_info[1] + "/"
        #self.url_str = "https:/template.url/generic_page/" + urllib.parse.urlencode()
       #if self.server_info[2] is not None:
       #     self.url_str += '/'+ self.server_info[2]
       #if self.server_info[3] is not None:
            #self.url_str += "/" + self.server_info[3]
       self.url_str = server_info
    #should I include a "force" parameter?
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
    def add_done_callback(self, function_name):
        function_name