import RPi.GPIO as GPIO
from time import sleep, time
import multiprocessing
from subprocess import call
from api.globals import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

call(['sh', '/root/sciencefair-2018/codebase/api/welcome.sh'])

while True:
    if GPIO.input(BUTTON_PIN):
        start = time()

        while GPIO.input(BUTTON_PIN):
            sleep(0.01)

        if (time() > start + 1):
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['python3', '/root/sciencefair-2018/codebase/main_addpoints.py'])
        else:
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            call(['/root/sciencefair-2018/codebase/api/tonecreation', '70', '0.4'])
            #call(['python3', '/root/sciencefair-2018/codebase/main_4corners.py'])
            call(['python3', '/root/sciencefair-2018/codebase/quickcut.py'])

        call(['/root/sciencefair-2018/codebase/api/tonecreation', '80', '1'])

    sleep(0.1)
