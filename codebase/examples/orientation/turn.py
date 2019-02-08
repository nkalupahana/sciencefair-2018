import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from multiprocessing import Queue
from api.ninedof import *
import Adafruit_MotorHAT
from api.motors import *

orient = NineDOF()
q = Queue()

orient.gyro_accel_zero()
orient.gyro_heading_begin_tracking(0.01, q)

mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))

ds.go(0, True)

while abs(q.get() - 55) > 0.1:
    error = q.get() - angle
    ds.adjustSpeed(error * 20)
    sleep(0.01)

orient.gyro_accel_heading_terminate()
ds.stop()
