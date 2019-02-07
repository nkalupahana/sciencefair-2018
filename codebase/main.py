import RPi.GPIO as GPIO
from time import sleep, time
import multiprocessing
from subprocess import Popen
from api.globals import BUTTON_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

while True:
    if GPIO.input(self.pin):
        start = time

        while GPIO.input(self.pin):
            if (time() > start + 1):
                print("LONG")
                while GPIO.input(self.pin):
                    sleep(0.1)

                print("RELEASE")

        print("SHORT")
        print("RELEASE")

    sleep(0.1)
