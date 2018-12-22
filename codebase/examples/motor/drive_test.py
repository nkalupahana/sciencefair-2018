#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys
sys.path.append("../../")
from api.motors import *

atexit.register(turnOffMotors)
mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
ds.go(100)
sleep(3)
ds.stop()

cutter = Cutter(mh.getMotor(3))
cutter.cut()

ds.go(-100)
sleep(3)
ds.stop()
