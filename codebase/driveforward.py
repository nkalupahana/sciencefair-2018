#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit
from api.motors import *
from api.camera import *
from api.positioning import *

atexit.register(turnOffMotors)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# system initialization
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
cutter = Cutter(mh.getMotor(3))
camera = Camera("../files/main.graph", 0.20, 0.20, {0: "bg", 1: "dandelion"})

# Start main driver system thread
drivethread = multiprocessing.Process(target=driver)
drivethread.daemon = True
drivethread.start()

# Start main driver system thread
gpsthread = multiprocessing.Process(target=gpssystem)
gpsthread.daemon = True
gpsthread.start()

def driver():
    global gymin
    ds.start(100)

    while True:
        if (camera.run()):
            sleep(gymin * 5)
            ds.setSpeed(50)
            cutter.cut()
            ds.setSpeed(1) # Pause for further camera input
        else:
            ds.setSpeed(100)
