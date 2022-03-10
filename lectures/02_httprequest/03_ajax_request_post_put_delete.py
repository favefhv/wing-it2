# https://www.nylas.com/blog/use-python-requests-module-rest-apis/
import requests
import json

url = "http://domainname.org/path"  # todo: change the url

# POST-Request
#data = {"title": "POST Request", "description": "POST Request from Python", "completed": False, "targetDate": "2021-02-22T00:00:00"}
#headers = {'Content-Type': 'application/json'}
#response = requests.post(url, data=json.dumps(data), headers=headers)

# PUT-Request
#data = {"id" : 2, "title" : "PUT Request", "description" : "POST Request from Python to Azure REST-API", "completed" : True, "targetDate" : "2021-02-27"}
#headers = {'Content-Type': 'application/json'}
#response = requests.put(url + "/2", data=json.dumps(data), headers=headers)

# DELETE-Request
#response = requests.delete(url + "/2")

# print status code and content
print(response.status_code)
print(response.content)