from time import sleep
from picamera import PiCamera
import os

def snap(output_location):
    camera.resolution = (1024, 768)
    camera.rotation = 180
    camera.start_preview()
    if os.path.exists(output_location):
        os.remove(output_location)
    camera.start_preview()
    sleep(2)    # camera warm-up time
    camera.capture(output_location)
    camera.stop_preview()

camera = PiCamera()
snap('/home/pi/webapp/static/image.jpg')
