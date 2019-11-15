#comment on the communication protocols, what kind of stuff should be included on the json file

#for this part, literally just work on the client side, NOTHING that should be done on the server side
#therefore, this should have the interface without any job_template class to make objects, 
#don't need to have any sort of object creation here for jobs

#research how to write the client script:
    #research "requests"", use "posts" and json, and pickle
        #pickle converts arguments into string, and trns into json
        #1: requests 2: pickle, 3: understand json
import requests
import json

class Executor():
    def __init__(self, host, port, path = None, params = None):
        self.server_info = (host, port, path, params)
        assert ((self.server_info[0] is not None) and (self.server_info[1] is not None))
        self.url_str = "http://" + self.server_info[0] + ":" + self.server_info[1] + "/"
        if self.server_info[2] is not None:
            self.url_str += self.server_info[2]
        if self.server_info[3] is not None:
            self.url_str += "?" + self.server_info[3]

        #server stores info of jobs in centralized location, so should manage encoding

    def submit(self, fn, job_name, memory, *args, priority = 1, retries = 0, run_now = False, **kwargs):
        #just as fn denotes the callable in futures, the submit(job_name....) should schedule the callable 
        ####
            #post here
            #need a means to dynamically create key:value pairs for variable arguments:        
        #format into a json file and then put it in through post, we can technically have the source address just be tuple of 
            #host and port info.  
        data  = {'fn': fn, 'job_name': job_name, 'memory': memory, 'priority': priority, 
                 'retries': retries, 'run_now': run_now, 'func_args': *args, 'func_kwargs': **kwargs}
        json_data = json.dumps(data)
        r = requests.post(self.url_str, json = json_data)
        ####
        #this portion would facilitate communication of job specifications: job_name, size, priority, retries, send_data, force
               #need implicit arguments here *args and **kwargs
                #send w http or json
                #for priority & force: can put those with the same priorities in the same queue, on the order they were received
                #then upon submitting another with force, that would trump all others with same priority

        #the future object should hold the info to know the status of the job, just need to get 
       #NOT the job and the processing itself, rather its a supervisor
        new_future = Future(job_name, self.server_info, *args, **kwargs)
        #the object doesn't have the job specifications itself, function_name should be the path

        return new_future

    #def map():
        #can include map() later not now.  
        
    #next I want to include a function that will grab info from the server
    def grab(self, job_name):
        #params for the desired info to grab from the server
        PARAMS = {'job name': job_name, 'running': None, 'retries left': None, 'func_args': None, 'func_kwargs': None} 
        r = request.get(url = url_str, params = PARAMS)
        data = r.json()

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
    def __init__(self, function_name, server_info, func_args, func_kwargs):
       self.job_name = function_name
    def cancel(self, force = False):

        return False
    def cancelled(self):
        return True

    def running(self):
        return True
    def done(self):
        return True
    def result(self):
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