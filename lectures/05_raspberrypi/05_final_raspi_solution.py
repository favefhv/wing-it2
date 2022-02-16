from gpiozero import LED, MotionSensor
from time import sleep

led = LED(18)
motion_sensor = MotionSensor(27)

def send_status_change_to_server(status):
    import requests
    import json
    
    sensor_id = 6 
    api_key = "wing_test"
    url = "http://domainname.org/api/sensors/" + str(sensor_id) # todo: change the url
    
    # POST-Request
    data = { "value" : status }
    headers = { 'Content-Type' : 'application/json', 'api_key' : api_key }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    
    print(response.status_code)
    print(response.content)

status = False

from time import sleep

while True:
    if motion_sensor.is_active:
        if not status:
            status = True
            send_status_change_to_server(status)
        led.on()
    else:
        if status:
            status = False
            send_status_change_to_server(status)
        led.off()
    sleep(0.1)