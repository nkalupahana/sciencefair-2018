import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from api.ninedof import *

orient = NineDOF()
orient.gyro_accel_calibration(0.04)

while True:
    sleep(5)
