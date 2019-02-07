import RPi.GPIO as GPIO
from time import sleep, time
import multiprocessing
from subprocess import call
from api.globals import BUTTON_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

call(['sh', './api/welcome.sh'])

while True:
    if GPIO.input(BUTTON_PIN):
        start = time()

        while GPIO.input(BUTTON_PIN):
            sleep(0.01)

        if (time() > start + 1):
            call(['./tonecreation', '70', '0.4'])
            call(['./tonecreation', '70', '0.4'])
            call(['./tonecreation', '70', '0.4'])
            call(['./tonecreation', '70', '0.4'])
            call(['rm', DATABASE_NAME])
            call(['python', './main_addpoints.py'])
        else:
            call(['./tonecreation', '70', '0.4'])
            call(['./tonecreation', '70', '0.4'])
            call(['python', './main_4corners.py'])

        call(['./tonecreation', '77', '1'])

    sleep(0.1)
