# https://www.geeksforgeeks.org/get-post-requests-using-python/
# https://www.nylas.com/blog/use-python-requests-module-rest-apis/
import requests

# URL - api endpoint
url = "http://domainname.org/path"  # todo: change the url

# sending get request and saving the response as response object 
res = requests.get(url)
print(res.status_code)

# For successful API call, response code will be 200 (OK)
if res.ok:
    # extracting data in json format 
    jData = res.json()
    print(jData)
else:
    # response code is not ok, print http error code with description
    res.raise_for_status()