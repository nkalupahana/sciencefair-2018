import sys
sys.path.append("../../")

from time import sleep
from multiprocessing import Queue
from api.ninedof import *

orient = NineDOF()
q = Queue()
orient.gyro_heading_begin_tracking(0.1, q)

while True:
    print(q.get())
