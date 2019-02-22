from api.motors import *
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import sys
sys.path.append("./")
sys.path.append("./api")

# Initialize components
mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
cutter = Cutter(mh.getMotor(3))

ds.go(100)
sleep(5)
ds.go(50)
cutter.cut()
ds.go(100)
sleep(5)
ds.stop()
