from gpiozero import LED, Button
from time import sleep

led = LED(18)
button = Button(17)

while True:
    if button.is_pressed:
        print("Pressed")
    else:
        print("Released")
    sleep(1)