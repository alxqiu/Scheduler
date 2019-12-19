import urllib.parse
import json
import requests

print("works")
url = 'https://postman-echo.com/post'
payload = 'foo1=bar1&foo2=bar2'
headers = {}
response = requests.post(url, data = payload)
print(response.text)
print(response.status_code)

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

