from gpiozero import LED, MotionSensor
from time import sleep
import wing_api

led = LED(18)
motion_sensor = MotionSensor(27)
status = False

while True:
    if motion_sensor.is_active:
        if not status:
            status = True
            wing_api.send_status_change_to_server(status)
        led.on()
    else:
        if status:
            status = False
            wing_api.send_status_change_to_server(status)
        led.off()
    sleep(0.1)