import RPi.GPIO as GPIO
from time import sleep, time
import multiprocessing
from subprocess import call
from api.globals import *

# Allow input from button pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

# Play startup chime
call(['sh', '/root/sciencefair-2018/codebase/api/welcome.sh'])

while True:
    # If button pressed:
    if GPIO.input(BUTTON_PIN):
        # Record start time
        start = time()

        # While button pressed, wait
        while GPIO.input(BUTTON_PIN):
            sleep(0.01)

        # If pressed for longer than one second, run point save program
        # Else, run detection program
        if (time() > start + 1):
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['python3', '/root/sciencefair-2018/codebase/main_addpoints.py'])
        else:
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['python3', '/root/sciencefair-2018/codebase/main_4corners.py'])
            #call(['python3', '/root/sciencefair-2018/codebase/quickcut.py']) TEST

        call(['/root/sciencefair-2018/codebase/api/tonecreation', '80', '1'])

    sleep(0.1)
