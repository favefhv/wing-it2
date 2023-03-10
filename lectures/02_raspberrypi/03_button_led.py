from gpiozero import LED, Button
from time import sleep

led = LED(18)
button = Button(17)

#while True:
#    if button.is_pressed:
#        led.on()
#    else:
#        led.off()
#    sleep(1)

#button.when_pressed = led.on()
#button.when_released = led.off()

button.when_pressed = led.toggle
