import RPi.GPIO as GPIO
from time import sleep, time
import multiprocessing
from subprocess import Popen
from api.globals import BUTTON_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

while True:
    if GPIO.input(BUTTON_PIN):
        start = time()

        while GPIO.input(BUTTON_PIN):
            sleep(0.01)


        if (time() > start + 1):
            print("RELEASE")
        else:
            print("SHORT")


    sleep(0.1)
