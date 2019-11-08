
#comment on the communication protocols, what kind of stuff should be included on the json file

#for this part, literally just work on the client side, NOTHING that should be done on the server side
#therefore, this should have the interface without any job_template class to make objects, 
#don't need to have any sort of object creation here for jobs
class Executor():
    def __init__(self, IP, port):
        self.server_info = (IP, port)

        #server stores info of jobs in centralized location, so should manage encoding

    def submit(self, job_name, size, priority = 1, retries = 0, send_data = True):
        #just as fn denotes the callable in futures, the submit(job_name....) should schedule the callable 
        
        #gets the Futures object according to the name??? NOT the job and the processing itself, rather its a supervisor
        new_future = Future(function_name, self.server_info)
        #the object doesn't have the job specifications itself

        #determine in what format you should send to server
        #will have job_name, priority, retries, and send_data sent directly to server, not the future object
        self.server_info
        #this portion would facilitate communication of job specifications: job_name, size, priority, retries, send_data
        #send w http or json

        #the future object should hold the info to know the status of the job
        #get the results from that future object to assess the info
        return new_future

    #def map():
        #can include map() later not now.  
    
    #next I want to include a function that will grab info from the server
        
    def shutdown(self, wait = True):
        #grab server info and try to assess if job is done or not
        args = True
        #get result from Future.running() to see if the jobs can be shut down
        if wait:
            args = False
        return args
            

#this is all about the references to the actual job object, a means to reference from client
#the future object is responsible for getting inquiries from the client about the server
#the future object should keep all the info for the server and name, and facilitate communication between server and client
class Future():
    def __init__(self, job_name, server_info):
       self.job_name = job_name
    def cancel(self):

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