#handle both getting information from POST and retrieval of info from _grab

#needs to be run in one instance of cmd, then run TestScript in another window to conduct tests.
    #figure out how the ServerSideScript should work, in terms of classes/functions structures

import datetime
from flask import Flask, request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import pickle

ServerSideScript = Flask(__name__)

#this should be the place where the job info is stored:
    #'<job_id>': {'fn': <fn>, 'func_args': <*args>, 'func_kwargs': <**kwargs>, 
    #   'job_id': <job_id>, 'memory': <memory>, 'priority': <priority>, 
    #   'retries': <retries>, 'run_now': run_now}
#change data storage to pickle format, have the function name pickled
    #convert each job back into object, and figure out which package and modules it is in, and load it for me

#pickled and non pickled:
    #only 'fn', 'func_args', and 'func_kwargs' will be pickled
data_for_jobs = {'19838182.391829': {'fn': 'placeHolder', 'func_args': [], 
    'func_kwargs': {}, 'job_id': 19838182.391829, 'memory': 1024, 
    'priority': 2, 'retries': 1, 'run_now': True, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None}}

@ServerSideScript.route('/')
def default():
    return 'Up and running!'

#sends back unique id for a function in str form so its static
def function_encoder(fn):
    return str(datetime.datetime.now().timestamp())

server_running = True
#make sure I have a function to manage all the running of the jobs
                #######currently not suitable
def job_manager():
    while (server_running):
        #every iteration of this large loop is one job ran
        #adjust sleep time arbitrarily, or by system constraints
        time.sleep(2.4)
        if (data_for_jobs is not None):
            #update the viable jobs list
            runnable_jobs = dict()        
            for job in data_for_jobs.items():
                #jobs are moved to tuple form when parsed in forloop
                job_properties = job[1]
                if (job_properties['cancelled'] == job_properties['complete']):
                    runnable_jobs.update({job[0]: job[1]})

            target_id = list(runnable_jobs.keys())[0]
            highest_prior = runnable_jobs.get(list(runnable_jobs.keys())[0]).get('priority')
            #now it can trump priority, and defers to oldest. 
            for job in runnable_jobs.items():
                job_properties = job[1]
                if job_properties.get('run_now') == True:
                    target_id = job[0]
                    break
                #so far, equal priority gives run to oldest received 
                if (highest_prior > job_properties.get('priority')):
                    highest_prior = job_properties.get('priority')
                    target_id = job[0]
                
        #run_job will do change the running property later
            run_job(target_id)
    return None

#should have a dedicated method to processing jobs in general, should have info
#for the sake of seeing if any job is running at all
            ###########
            #make sure only one running at the same time
def run_job(job_id):
    #make sure retries is monitored and adjusted
    #whatever is ran is iterated over the for loop on the int in retries box

    fn = pickle.loads(data_for_jobs.get(job_id)['fn'])
    func_args = pickle.loads(data_for_jobs.get(job_id)['func_args'])
    func_kwargs = pickle.loads(data_for_jobs.get(job_id)['func_kwargs'])
    data_for_jobs.get(job_id)['running'] = True
    for i in range(data_for_jobs.get(job_id)['retries'] + 1):
         try:
             fn(func_args, func_kwargs)
         except:
             #placeholder for exceptions
             data_for_jobs.get(job_id)['exceptions'] = 'Exception_One'

         ###here is where the "running" of the job takes place
         #how they work:
            #unpickling here: and then the function and its args exists
             #input would be a string of fn which would be a pickle object, and the pickle module would locate that
             #assuming same modules and packages are present on both interface and server objects
            #just make a function call, put into "try catch", "try except thing 

    #need to encapsulate the results, so you can catch if there are any exceptions that appear
    #accessing job properties like this works 
    data_for_jobs.get(job_id) ['complete'] = True
    return None

#not sure the definitions of running a function
            ############
@ServerSideScript.route('/cancel-job', methods = ['POST'])
def cancel_job():
    job_id = request.get_json()['job_id'] 
    assert data_for_jobs.get(job_id)['cancelled'] is False
    #this should edit the ['cancelled'] attr of the job

    data_for_jobs.get(job_id)['cancelled'] = True
    return None


#@ServerSideScript.route('/handleRequest', methods = ['POST', 'GET'])
#just returns the json of whatever was sent through request
#dev way to get a unique job id.  
@ServerSideScript.route('/submit-request', methods = ['POST'])
def submit_request():
    request_data = request.get_json()

    #adding encoded data
    encoded_var = function_encoder(request_data['fn'])

    #adding new information directly linked to functionality in the server side
    request_data['job_id'] = encoded_var
    request_data['complete'] = False
    #make sure this is invoked with run
    request_data['running'] = False
    request_data['cancelled'] = False
    request_data['exception'] = None

    #now we start a job and store the information in a variable
    ##---> insert a job start function here
            #####or do I if the running function is passively running

    #the variable containing the dict of job information sent through is updated with an unique id,  
    data_for_jobs[encoded_var] = request_data
    return (request_data)


#send back data_for_jobs but only specifically for the id requested. 
@ServerSideScript.route('/grab-job-info', methods = ['GET'])
def grab_job_info():
    send = json.dumps(data_for_jobs.get(str(request.get_json()['job_id'])))
    return send


#perhaps this could use a generic get request method?
@ServerSideScript.route('/get-request', methods = ['GET'])
def get_request():
    return None
#need another method to address NON-submit requests, generic post request method
@ServerSideScript.route('/post-request', methods = ['POST'])
def post_request():
    return None

#shutdown function, as no command line to rely on
@ServerSideScript.route('/kill', methods = ['POST'])
def kill():
    func = request.get('werkzeug.server.shutdown')
    func()
    return "Quitting"


if __name__ == '__main__':
    ServerSideScript.run(debug = True, host = '0.0.0.0')




