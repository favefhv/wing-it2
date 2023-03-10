from gpiozero import LED
from time import sleep

led = LED(18)
#led.off()
#led.blink()

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)