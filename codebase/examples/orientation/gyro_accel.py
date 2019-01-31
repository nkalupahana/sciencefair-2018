import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from multiprocessing import Queue
from api.ninedof import *

orient = NineDOF()
q = Queue()

orient.gyro_accel_zero()
orient.ga_heading_begin_tracking(0.01, q)

while True:
    print(q.get())
