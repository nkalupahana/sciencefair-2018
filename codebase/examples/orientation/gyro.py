import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from multiprocessing import Queue
from api.ninedof import *

orient = NineDOF()
q = Queue()
orient.gyro_heading_begin_tracking(0.05, q)

while True:
    print(q.get())
