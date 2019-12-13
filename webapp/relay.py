"Code to control the relay board from the Raspberry Pi."

import time
import RPi.GPIO as GPIO

PIN = [32, 36]
def init():
    "Create the initial state of the relays."
    GPIO.setmode(GPIO.BOARD)

    # set PIN 32 output & default state
    GPIO.setup(32, GPIO.OUT)
    GPIO.output(32, GPIO.HIGH)

    # set PIN 36 output & default state
    GPIO.setup(36, GPIO.OUT)
    GPIO.output(36, GPIO.HIGH)

def press(switch):
    "The relay is activated or 'pressed', 0 or 1, on each call."
    moment = 0.01
    if switch in range(0, 2):
        try:
            GPIO.output(PIN[switch], GPIO.LOW)
            print("Relay " + str(switch) + " pressed")
            time.sleep(moment)
            GPIO.output(PIN[switch], GPIO.HIGH)
        except KeyboardInterrupt:
            GPIO.cleanup()

def cleanup():
    "Cleanup after the GPIO library."
    GPIO.cleanup()
    print("All off... Bye!!!")
