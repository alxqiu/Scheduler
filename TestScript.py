<<<<<<< HEAD

import urllib.parse
from Interface import Executor
import json

#run the host and port from the url of the echo server
def run (url = 'http://127.0.0.1:5000'):
        #first step: making sure I can send the right information to the postman server
            #ignore the generic url thing right now, can just run with hardcoded fake url
        #second step: making sure I can get back correct data
            #that will require defining more information defining submit 

    #parsed_url = urllib.parse.urlparse(url)
    #hostname = parsed_url.hostname
    #port = parsed_url.port
    #testInterface = Executor(hostname, port)
    
    testInterface = Executor(url)
    #testNameOne = 'xander18'
    #test_job_config = {'run_now': True, 'priority': 1, 'memory': 1024, 'retries': 2}
    #r = testInterface.submit(testNameOne, job_config = test_job_config)
    #print(r.testinfo())

    testNameTwo = 'kanyeweest'
    test_job_config = {'run_now': True, 'memory': 22}
    new_future = testInterface.submit(testNameTwo, True, 'dog', job_config = test_job_config, dog = True, cat = 34)
    print('future data: \n\t' + new_future.testinfo())
   
    print("default values: \n\t" + str({'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}))

    print("grabbed data: \n\t" + str(testInterface._grab(None)) + str(testInterface._grab(None)['running']))

run()


=======

import urllib.parse
from Interface import Executor
import json

#run the host and port from the url of the echo server
def run (url = 'http://127.0.0.1:5000'):
        #first step: making sure I can send the right information to the postman server
            #ignore the generic url thing right now, can just run with hardcoded fake url
        #second step: making sure I can get back correct data
            #that will require defining more information defining submit 

    #parsed_url = urllib.parse.urlparse(url)
    #hostname = parsed_url.hostname
    #port = parsed_url.port
    #testInterface = Executor(hostname, port)
    
    testInterface = Executor(url)
    #testNameOne = 'xander18'
    #test_job_config = {'run_now': True, 'priority': 1, 'memory': 1024, 'retries': 2}
    #r = testInterface.submit(testNameOne, job_config = test_job_config)
    #print(r.testinfo())

    testNameTwo = 'kanyeweest'
    test_job_config = {'run_now': True, 'memory': 22}
    new_future = testInterface.submit(testNameTwo, True, 'dog', job_config = test_job_config, dog = True, cat = 34)
    print('future data: \n\t' + new_future.testinfo())
   
    print("default values: \n\t" + str({'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}))

    print("grabbed data: \n\t" + str(testInterface._grab(None)) + str(testInterface._grab(None)['running']))

run()


>>>>>>> 7315051f83792f751c52da3f26f2ba36d605ea39
