import urllib.parse
import json
import requests
import pickle
import base64


#the test function as a module acessible for both the TestServer and this Script
from lib import PickleTestFunc

#this file isn't necessarily a module, its just a script.
    #need a package, need to make a subdirectory, and make it package name, and make a package
    #have the .py file in there, and have a intialization, that would make it a valid module


data_for_jobs = {'testjobone': {'job_id': 19838182.391829, 
    'priority': 2, 'run_now': False, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None}, 
                 'testjobtwo': {'job_id': 19838182.391829, 
    'priority': 2, 'retries': 1, 'run_now': False, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None},
                 'testjobthree': {'job_id': 19838182.391829, 
    'priority': 2, 'retries': 1, 'run_now': False, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None}}


#skeleton of the submit function from ServerSideScript
    #now we should prioritize fitting args and kwargs to appropriate spots
    # or should that be on the side of the server?
def pickel_test(fn, *args, **kwargs):
        
    fn = str(base64.b64encode(pickle.dumps(fn)).decode('utf-8'))
    args = str(base64.b64encode(pickle.dumps(args)).decode('utf-8'))
    kwargs = str(base64.b64encode(pickle.dumps(kwargs)).decode('utf-8'))
    
    #at this point, <*args> is transformed into a list in <args>, and <**kwargs> into dict <kwargs>

    data = {'fn': fn, 'func_args': args, 'func_kwargs': kwargs}

    r = requests.post('http://127.0.0.1:5000' + '/submit-request-2', json = data)
    print(r.text)



####error as the TestServer2.py file doesn't have access to pickle_test_func
pickel_test(PickleTestFunc.pickle_test_func, 0, 'twenty-six', a ='b', b = 'c', c = 'a')

###test cases for content of r objects
#r = requests.post('http://127.0.0.1:5000' + '/post-request', json = data_for_jobs)
#print(r.text)

#job_config = dict({})
#assert len(job_config.keys()) is not 0

####testing basic encoding/decoding/string stuff
#print(str(pickle.dumps(PickleTestFunc.pickle_test_func)))
#this one works. 
#key = str(base64.b64encode(pickle.dumps(PickleTestFunc.pickle_test_func)).decode('utf-8'))
#print(key)
#this is same as OG pickled bytes by the way
#print(base64.b64decode(key.encode('utf-8')))

#data  = {'fn': 'fn', 'func_args': 'args', 'func_kwargs': 'kwargs', 'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
#r = requests.post('http://127.0.0.1:5000' + '/submit-request', json = data)

#print(str(r.json().get('job_id')) + " " + str(r.status_code))

#default_config = {'memory': None, 'priority': 1, 'retries': 0, 'run_now': False}
#job_config = {'memory': None, 'mutate': True}
#assert set(job_config.keys()) < set(default_config.keys())

#print('data for jobs:\n\t' + str(data_for_jobs))
#runnable_jobs = dict()
#data_for_jobs.get('testjobtwo') ['complete'] = True
#for parsed_dict in data_for_jobs.items():
    #print('parsed dict\n\t' + str(parsed_dict))
            #get down to lower layer of all_dicts here
            #should access first key in the smallest parsed_dict, or the name of the job, 
            #and then the properties of said job
   # check_dict = parsed_dict[1]
            #only time these conditions are equal is if neither has been started
 #   if (check_dict['cancelled'] == check_dict['complete']):
  #      runnable_jobs.update({parsed_dict[0]: parsed_dict[1]})
#print('runnable dicts\n\t' + str(runnable_dicts))

#grab initial target id and priority from the first item on runnable jobs
#target_id = list(runnable_jobs.keys())[0]
#highest_prior = runnable_jobs.get(list(runnable_jobs.keys())[0]).get('priority')
#for job in runnable_jobs.items():
                #sub represents the value of the initial "fn", so all the job info in one
                # and need to kick out key-value pairs that are already completed
  #          job_properties = job[1]
 #           if job_properties.get('run_now') == True:
   #             target_id = job[0]
    #            break

     #       if (highest_prior > job_properties.get('priority')):
      #          highest_prior = job_properties.get('priority')
       #         target_id = job[0] 
                
                
#print(target_id)

#print("works")
#url = 'https://postman-echo.com/post'
#payload = 'foo1=bar1&foo2=bar2'
#headers = {}
#response = requests.post(url, data = payload)
#print(response.text)
#print(response.status_code)

#####Set operation testing
#testOne = {'super': True, 'zoo': 'lupe', 'visine': 3}
#testTwo = {'zoo': 1, 'super': 3, 'kanye': 2, 'visine': 3, 'thump': 1}
#print(set(testOne.keys()).difference(set(testTwo.keys())))
#assert len(set(testOne.keys()) - set(testTwo.keys())) == 0
#print('success')

#####url creation testing
#only port registered as None for some reason
#print(hostname)
#print(port)

#server_info = (hostname, port)
#assert ((server_info[0] is not None) and (server_info[1] is not None))
#at this point both elements are Noneurl_str = "http://" + server_info[0] + ":" + server_info[1] + "/"

#self.url_str = "https:/template.url/generic_page/" + urllib.parse.urlencode()
#find a better way to recombinate the url components
#if self.server_info[2] is not None:
 #   self.url_str += '/'+ self.server_info[2]
#if self.server_info[3] is not None:
 #   self.url_str += "/" + self.server_info[3]

        #server stores info of jobs in centralized location, so should manage encoding

        #need to have PATH of either "/get" or "/post"

