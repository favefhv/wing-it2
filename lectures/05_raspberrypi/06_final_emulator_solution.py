from tkgpio import TkCircuit #  install the module for vs code: py -m pip install tkgpio
import wing_api

# initialize the circuit inside the GUI
configuration = {
    "width": 300,
    "height": 220,
    "leds": [
        {"x": 50, "y": 40, "name": "LED", "pin": 18}
    ],
    "motion_sensors": [
        {"x": 50, "y": 130, "name": "Motion Sensor", "pin": 27, "detection_radius": 50, "delay_duration": 5, "block_duration": 3 }
    ],
    "light_sensors": [
        {"x": 160, "y": 40, "name": "Light Sensor", "pin": 8}
    ],
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    
    from gpiozero import LED, LightSensor, MotionSensor
    from time import sleep

    led = LED(18)
    motion_sensor = MotionSensor(27)
    light_sensor = LightSensor(8)

    status = False

    while True:
        #print(light_sensor.value * 100)
        #print(motion_sensor.is_active)
        if light_sensor.value * 100 < 30 and motion_sensor.is_active:
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


