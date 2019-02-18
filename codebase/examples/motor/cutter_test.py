#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys
sys.path.append("../../")
sys.path.append("../../api")

from api.motors import *

atexit.register(turnOffMotors)
mh = Adafruit_MotorHAT(addr=0x60)
cutter = Cutter(mh.getMotor(3))
cutter.cut()
