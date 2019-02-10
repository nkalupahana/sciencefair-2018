import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from multiprocessing import Queue
from api.ninedof import *
import Adafruit_MotorHAT
from api.motors import *
import atexit
atexit.register(turnOffMotors)

orient = NineDOF()
q = Queue()

orient.gyro_accel_zero()
orient.ga_heading_begin_tracking(0.01, q)

mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))

ds.go(0, True)

while abs(q.get() - 55) > 0.1:
    error = q.get() - 55
    print(error)
    ds.m1.run(Adafruit_MotorHAT.FORWARD)
    ds.m1.setSpeed(int(abs(error * 10)))
    ds.m2.run(Adafruit_MotorHAT.BACKWARD)
    ds.m2.setSpeed(int(abs(error * 10)))

orient.ga_heading_terminate()
ds.stop()
