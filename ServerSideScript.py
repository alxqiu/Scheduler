#handle both getting information from POST and retrieval of info from _grab

#needs to be run in one instance of cmd, then run TestScript in another window to conduct tests.
    #figure out how the ServerSideScript should work, in terms of classes/functions structures

import datetime
from flask import Flask, request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ServerSideScript = Flask(__name__)
data_for_jobs = {'jobOne': {'running': True, 'memory': 1024, 'priority': 2}, 
               'jobTwo': {'running': True, 'priority': 1, 'memory': 2048}}

@ServerSideScript.route('/')
def default():
    return 'Up and running!'

#sends back unique id for a function
def functionEncoder(fn):
    return str(datetime.datetime.now().timestamp())


#@ServerSideScript.route('/handleRequest', methods = ['POST', 'GET'])
#just returns the json of whatever was sent through request
#dev way to get a unique job id.  
@ServerSideScript.route('/submitRequest', methods = ['POST'])
def submitRequest():
    request_data = request.get_json()

    #adding encoded data
    encoded_var = functionEncoder(request_data['fn'])
    request_data['job_id'] = encoded_var

    #now we start a job and store the information in a variable
    ##---> insert a job start function here

    #replace kanyeweest with job_id
    data_for_jobs[encoded_var] = request_data
    return (request_data)

#need another method to address NON-submit requests


@ServerSideScript.route('/handleGETRequest', methods = ['GET'])
def handleGETRequest():
    send = json.dumps(data_for_jobs.get(str(request.get_json()['job_id'])))
    #return json.dumps(dataForJobs(request.get_json()['fn']))
    #so far it works for fn, now need to try function id
    return send

if __name__ == '__main__':
    ServerSideScript.run(debug = True, host = '0.0.0.0')


