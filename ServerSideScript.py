#handle both getting information from POST and retrieval of info from _grab

#needs to be run in one instance of cmd, then run TestScript in another window to conduct tests.
    #figure out how the ServerSideScript should work, in terms of classes/functions structures

import datetime
from flask import Flask, request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import pickle
import threading
import base64
from inspect import signature

ServerSideScript = Flask(__name__)

#this should be the place where the job info is stored:
    #'<job_id>': {'fn': <fn>, 'func_args': <*args>, 'func_kwargs': <**kwargs>, 
    #   'job_id': <job_id>, 'memory': <memory>, 'priority': <priority>, 
    #   'retries': <retries>, 'run_now': run_now}
#change data storage to pickle format, have the function name pickled
    #convert each job back into object, and figure out which package and modules it is in, and load it for me

#pickled and non pickled:
    #only 'fn', 'func_args', and 'func_kwargs' will be pickled
#data_for_jobs = {'19838182.391829': {'fn': 'placeHolder', 'func_args': [], 
 #   'func_kwargs': {}, 'job_id': 19838182.391829, 'memory': 1024, 
  #  'priority': 2, 'retries': 1, 'run_now': True, 'complete': False, 
   # 'running': False, 'cancelled': False, 'exception': None, 'result': None}}
data_for_jobs = {}
lock = threading.Lock()

@ServerSideScript.route('/')
def default():
    return 'Up and running!'

#sends back unique id for a function in str form so its static
def function_encoder(fn):
    return str(datetime.datetime.now().timestamp())
server_running = True

##make private later
#runnable_jobs = dict()

def job_manager():
    #will make this non-global after finishing debug
    global runnable_jobs
    while (server_running):
            #when checking, protect d_f_j using lock
        if len(data_for_jobs) > 0:
            #update the viable jobs list
                #####will make runnable jobs private to this function after correctly debugged
            runnable_jobs = dict()       
            ###protect data_for_jobs dict() only precisely when its accessed
            for job in data_for_jobs.items():
                #jobs are moved to tuple form when parsed in forloop
                job_properties = job[1]
                if (job_properties['cancelled'] == job_properties['complete']):
                    runnable_jobs[job[0]] = job[1]
            if (len(runnable_jobs) > 0):
                    #####problem: 2/6/2020:
                        #need to assure that jobs that receive cancel order are affected on runnable_jobs
                        #and can be removed or removed from consideration here
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
                run_job(target_id)
        else:
            time.sleep(0.5)
    return None

def run_job(job_id):
    #make sure retries is monitored and adjusted
    #whatever is ran is iterated over the for loop on the int in retries box
    with lock:
        job_properties = data_for_jobs.get(job_id)
        fn = pickle.loads(base64.b64decode(job_properties['fn'].encode('utf-8')))
        func_args = pickle.loads(base64.b64decode(job_properties['func_args'].encode('utf-8')))
        func_kwargs = pickle.loads(base64.b64decode(job_properties['func_kwargs'].encode('utf-8')))
        data_for_jobs.get(job_id)['running'] = True
        for i in range(job_properties['retries'] + 1):
             try:
                  #ensure that the arrangement of func_args and func_kwargs can match up to arguments in the function call
                data_for_jobs.get(job_id)['result'] = fn(*func_args, **func_kwargs)
                data_for_jobs.get(job_id)['running'] = False
                break
             except:
                #we are sending all exceptions, even generic ones back to the interface
                #should have abstractified code here for that
                data_for_jobs.get(job_id)['exceptions'] = 'Exception_One' 
        data_for_jobs.get(job_id) ['complete'] = True
        data_for_jobs.get(job_id)['running'] = False
    return None

@ServerSideScript.route('/cancel-job', methods = ['POST'])
def cancel_job():
    global data_for_jobs
    lock.acquire()
    job_id = request.get_json()['job_id'] 
    assert data_for_jobs.get(job_id)['cancelled'] is False
    #this should edit the ['cancelled'] attr of the job
    data_for_jobs.get(job_id)['cancelled'] = True
    lock.release()
    return None


#@ServerSideScript.route('/handleRequest', methods = ['POST', 'GET'])
#returns the job_id, all that's needed to make the future object  
@ServerSideScript.route('/submit-request', methods = ['POST'])
def submit_request():
    global data_for_jobs
    request_data = request.get_json()
    #adding new information directly linked to functionality in the server side
    request_data['job_id'] = function_encoder(request_data['fn'])
    request_data['complete'] = False
    request_data['running'] = False
    request_data['cancelled'] = False
    request_data['exception'] = None
    request_data['result'] = None  

    #as data_for_jobs is modified somewhere else at the same time, it needs to be locked
    lock.acquire()
    data_for_jobs[request_data['job_id']] = request_data
    #data_for_jobs.update({request_data['job_id']: request_data})
    lock.release()
    return {'job_id': request_data['job_id']}


#send back data_for_jobs but only specifically for the id requested. 
@ServerSideScript.route('/grab-job-info', methods = ['GET'])
def grab_job_info():
    lock.acquire()
    send = json.dumps(data_for_jobs.get(str(request.get_json()['job_id'])))
    lock.release()
    return send

#for debugging: sends back all data_for_jobs
@ServerSideScript.route('/get-data-for-jobs', methods = ['GET'])
def get_data_for_jobs():
    return data_for_jobs

#also for debugging
#@ServerSideScript.route('/get-runnable-jobs', methods = ['GET'])
#def get_runnable_jobs():
 #   return runnable_jobs


###two generic requests that don't do anything
@ServerSideScript.route('/get-request', methods = ['GET'])
def get_request():
    return None
@ServerSideScript.route('/post-request', methods = ['POST'])
def post_request():
    return None

#shutdown function, as no command line to rely on
@ServerSideScript.route('/kill', methods = ['POST'])
def kill():
    server_running = False
    func = request.get('werkzeug.server.shutdown')
    func()
    return "Quitting"


if __name__ == '__main__':
    thread = threading.Thread(target = job_manager, daemon = True)
    thread.start()
    ServerSideScript.run(debug = True, host = '0.0.0.0')


