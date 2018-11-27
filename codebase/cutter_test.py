#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
motor = mh.getMotor(3)

motor.setSpeed(255)
motor.run(Adafruit_MotorHAT.FORWARD)
sleep(4)
motor.setSpeed(0)
motor.run(Adafruit_MotorHAT.RELEASE)
