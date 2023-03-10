from gpiozero import LED, MotionSensor
from time import sleep

led = LED(18)
motion_sensor = MotionSensor(27)

motion_sensor.when_motion = led.on
motion_sensor.when_no_motion = led.off