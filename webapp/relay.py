""" Switch two relays 0 and 1, momentarily."""
import RPi.GPIO as GPIO
import time

pin = [ 32, 36 ]
def init():
    """ Initialize the Raspberry Pi GPIO pins. """
    GPIO.setmode(GPIO.BOARD)

    # set pin 32 output & default state
    GPIO.setup(32,GPIO.OUT)
    GPIO.output(32,GPIO.HIGH)

    # set pin 36 output & default state
    GPIO.setup(36,GPIO.OUT)
    GPIO.output(36,GPIO.HIGH)

def press(switch):
    """ Momentarily switch on & off a relay [0|1]. """
    moment = 0.01
    if switch in range(0,2):
        try:
            GPIO.output(pin[switch], GPIO.LOW)
            print("Relay " + str(switch) + " pressed")
            time.sleep(moment)
            GPIO.output(pin[switch], GPIO.HIGH)
        except KeyboardInterrupt:
            GPIO.cleanup()

def cleanup():
    """ Once the relay is done operation clean up after it. """
    GPIO.cleanup()
    print("All off... Bye!!!")

