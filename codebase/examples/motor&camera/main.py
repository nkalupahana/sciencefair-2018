#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys
sys.path.append("../../")
from api.motors import *
from api.camera import *
from api.globals import *

atexit.register(turnOffMotors)

# create motor HAT object (standard I2C address)
mh = Adafruit_MotorHAT(addr=0x60)

# system component initialization
ds = DriveSystem(mh.getMotor(BASE_MOTOR_1), mh.getMotor(BASE_MOTOR_2))
cutter = Cutter(mh.getMotor(CUTTER_MOTOR))
camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)

# Start main driver system thread
drivethread = multiprocessing.Process(target=_driver)
drivethread.daemon = True
drivethread.start()

def _driver():
    ds.go(100)

    while True:
        ymin = camera.run()
        if (camera.run() != 0):
            sleep(ymin / 40)
            ds.go(50)
            cutter.cut()
            ds.go(-10) # Wait for further camera input
        else:
            ds.go(100)
