def send_status_change_to_server(status):
    import requests
    import json
    
    sensor_id = 6 
    url = "http://domainname.org/api/sensors/" + str(sensor_id)   # todo: change the url -- "http://domainname.org/api/sensors/"
    
    # POST-Request
    data = { "value" : status }
    headers = { 'Content-Type' : 'application/json' }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    
    print(response.status_code)
    print(response.content)
