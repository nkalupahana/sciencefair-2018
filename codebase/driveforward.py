#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit
from api.motors import *
from api.camera import *

atexit.register(turnOffMotors)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# system initialization
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
cutter = Cutter(mh.getMotor(3))
camera = Camera()
camera.start()

ds.start(100)
sleep(2)
ds.stop()
