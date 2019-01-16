import sys
sys.path.append("../../")

from time import sleep
from api.ninedof import *

orient = NineDOF()
head = 0
orient.gyro_heading_begin_tracking(0.1, head)

while True:
    print(head)
    sleep(0.1)
