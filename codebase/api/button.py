import RPi.GPIO as GPIO
from time import sleep
import multiprocessing
from subprocess import Popen

# Button Watch Thread System
class ButtonActionThread:
    def __init__(self, pin, runner, pitch):
        self.runner = runner
        self.pin = pin
        self.pitch = pitch

        # Set up button pin to accept inputs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)

    # Activates checkPin thread
    def activate(self):
        self.thread = multiprocessing.Process(target=self.checkPin)
        self.thread.daemon = True
        self.thread.start()

    # Terminates thread
    def deactivate(self):
        self.thread.terminate()
        self.thread = None

    # Plays specified tone
    def playTone(self, pitch):
        Popen(['/root/sciencefair-2018/codebase/api/tonecreation', str(pitch), '0.3'])

    # Thread function (checks for and handles button press)
    def checkPin(self):
        while True:
            # If button pressed
            if GPIO.input(self.pin):
                self.playTone(self.pitch)       # Play tone
                self.runner()                   # Run provided onclick function
                self.playTone(self.pitch + 10)  # Play completion tone
                while GPIO.input(self.pin):     # Wait for button to be unpressed
                    sleep(0.1)

            sleep(0.1)
