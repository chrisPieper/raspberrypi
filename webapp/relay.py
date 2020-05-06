""" Switch two relays 0 and 1, momentarily."""
import time
import RPi.GPIO as GPIO
import yaml


with open('static/config.yaml', 'r') as yaml_file:
    try:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
    except yaml.YAMLError as exception:
        APP.logger.error('Could not open YAML configuration file.')
        exit()

PIN = data['PIN']
MOMENT = data['MOMENT']

def init():
    """ Initialize the Raspberry Pi GPIO pins. """
    GPIO.setmode(GPIO.BOARD)

    # set pin 0 output & default state
    GPIO.setup(PIN[0], GPIO.OUT)
    GPIO.output(PIN[0], GPIO.HIGH)

    # set pin 1 output & default state
    GPIO.setup(PIN[1], GPIO.OUT)
    GPIO.output(PIN[1], GPIO.HIGH)


def press(switch, logger):
    """ Momentarily switch on & off a relay [0|1]. """
    if switch in range(0, 2):
        try:
            GPIO.output(PIN[switch], GPIO.LOW)
            logger.warning(f'Relay {switch} pressed')
            time.sleep(MOMENT)
            GPIO.output(PIN[switch], GPIO.HIGH)
        except KeyboardInterrupt:
            GPIO.cleanup()


def cleanup():
    """ Once the relay is done operation clean up after it. """
    GPIO.cleanup()
    print("All off... Bye!!!")
