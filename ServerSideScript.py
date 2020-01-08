#handle both getting information from POST and retrieval of info from _grab

#needs to be run in one instance of cmd, then run TestScript in another window to conduct tests.
    #figure out how the ServerSideScript should work, in terms of classes/functions structures

import datetime
from flask import Flask, request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ServerSideScript = Flask(__name__)

#this should be the place where the job info is stored:
    #'<job_id>': {'fn': <fn>, 'func_args': <*args>, 'func_kwargs': <**kwargs>, 
    #   'job_id': <job_id>, 'memory': <memory>, 'priority': <priority>, 
    #   'retries': <retries>, 'run_now': run_now}
data_for_jobs = {'19838182.391829': {'fn': 'placeHolder', 'func_args': [], 
    'func_kwargs': {}, 'job_id': 19838182.391829, 'memory': 1024, 
    'priority': 2, 'retries': 1, 'run_now': True, 'complete': False, 'running': False}}

@ServerSideScript.route('/')
def default():
    return 'Up and running!'

#sends back unique id for a function in str form so its static
def function_encoder(fn):
    return str(datetime.datetime.now().timestamp())

#should have a dedicated method to processing jobs in general, should have info
#for the sake of seeing if any job is running at all
def run_jobs():
    #have a part where the job is ran and the status ['complete'] is changed to True

    return None

#what do we do with cancel orders on already-canceled jobs?
def cancel_job(job_id):
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
    request_data['running'] = False
    request_data['cancelled'] = False

    #now we start a job and store the information in a variable
    ##---> insert a job start function here

    #the variable containing the dict of job information sent through is updated with an unique id,
    #and the data sent back tells the interface what that id is.  
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

if __name__ == '__main__':
    ServerSideScript.run(debug = True, host = '0.0.0.0')


