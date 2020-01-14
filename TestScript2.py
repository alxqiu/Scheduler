import urllib.parse
import json
import requests


data_for_jobs = {'testjobone': {'fn': 'placeHolder', 'func_args': [], 
    'func_kwargs': {}, 'job_id': 19838182.391829, 'memory': 1024, 
    'priority': 2, 'retries': 1, 'run_now': False, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None}, 'testjobtwo': {'fn': 'placeHolder', 'func_args': [], 
    'func_kwargs': {}, 'job_id': 19838182.391829, 'memory': 1024, 
    'priority': 2, 'retries': 1, 'run_now': True, 'complete': False, 
    'running': False, 'cancelled': False, 'exception': None}}

print('data for jobs:\n\t' + str(data_for_jobs))
runnable_jobs = dict()
for parsed_dict in data_for_jobs.items():
    print('parsed dict\n\t' + str(parsed_dict))
            #get down to lower layer of all_dicts here
            #should access first key in the smallest parsed_dict, or the name of the job, 
            #and then the properties of said job
    check_dict = parsed_dict[1]
            #only time these conditions are equal is if neither has been started
    if (check_dict['cancelled'] == check_dict['complete']):
        runnable_jobs.update({parsed_dict[0]: parsed_dict[1]})
#print('runnable dicts\n\t' + str(runnable_dicts))

target_id = ""
highest_prior = runnable_jobs.get(list(runnable_jobs.keys())[0]).get('priority')
for job in runnable_jobs.items():
                #sub represents the value of the initial "fn", so all the job info in one
                # and need to kick out key-value pairs that are already completed
            job_properties = job[1]
            if job_properties.get('run_now') == True:
                target_id = job[0]
                break

            if (highest_prior >= job_properties.get('priority')):
                highest_prior = job_properties.get('priority')
                target_id = job[0]
                break
print(target_id)

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

