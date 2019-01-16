import sys
sys.path.append("../../")

from time import sleep
from api.ninedof import *

orient = NineDOF()
global mhh
mhh = 0
orient.gyro_heading_begin_tracking(0.1)

while True:
    global mhh
    print(mhh)
    sleep(0.1)
