import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from api.ninedof import *
from multiprocessing import Queue

orient = NineDOF()
print("Zeroing...")
orient.gyro_accel_zero()
print("Filter starting...")
q = Queue()
orient.filter_begin_tracking(0.02,q)

while True:
    sleep(5)
