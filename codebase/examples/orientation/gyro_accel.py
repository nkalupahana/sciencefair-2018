import sys
sys.path.append("../../")

from time import sleep
from api.ninedof import *

orient = NineDOF()
orient.gyro_accel_heading_begin_tracking(0.1)

while True:
    print(orient.gyro_accel_heading())
    sleep(0.1)
