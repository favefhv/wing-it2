# importing the requests library - install the module via: py -m pip install requests
import requests 
  
# api-endpoint 
url = "http://www.if-schleife.de/index.html"
  
# sending get request and saving the response as response object 
res = requests.get(url) 

# status code and extracting content
print(res.status_code)
print(res.content)