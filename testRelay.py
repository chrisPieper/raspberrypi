import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32,GPIO.OUT)
GPIO.output(32,GPIO.HIGH)

GPIO.setup(36,GPIO.OUT)
GPIO.output(36,GPIO.HIGH)

try :
    print("Ready?")
    time.sleep(5)
    moment = 0.01

    GPIO.output(32, GPIO.LOW)
    print("Relay 1 is on")
    time.sleep(moment)
    GPIO.output(32, GPIO.HIGH)
    print("Relay 1 is off")
    time.sleep(2)

    GPIO.output(36, GPIO.LOW)
    print("Relay 2 is on")
    time.sleep(moment)
    GPIO.output(36, GPIO.HIGH)
    print("Relay 2 is off")
    time.sleep(5)

    GPIO.cleanup()
    print("All off... Bye!!!")

except KeyboardInterrupt :
    print("Done!")
    GPIO.cleanup()

