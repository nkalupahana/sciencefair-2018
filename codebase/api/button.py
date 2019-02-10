import RPi.GPIO as GPIO
from time import sleep
import multiprocessing
from subprocess import Popen

class ButtonActionThread:
    def __init__(self, pin, runner, pitch):
        self.runner = runner
        self.pin = pin
        self.pitch = pitch
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)

    def activate(self):
        self.thread = multiprocessing.Process(target=self.checkPin)
        self.thread.daemon = True
        self.thread.start()

    def deactivate(self):
        self.thread.terminate()
        self.thread = None

    def playTone(self, pitch):
        Popen(['/root/sciencefair-2018/codebase/api/tonecreation', str(pitch), '0.3'])

    def checkPin(self):
        while True:
            if GPIO.input(self.pin):
                self.playTone(self.pitch)
                self.runner()
                self.playTone(self.pitch + 10)
                while GPIO.input(self.pin):
                    sleep(0.1)

            sleep(0.1)
