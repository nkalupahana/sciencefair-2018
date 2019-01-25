import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from api.ninedof import *

orient = NineDOF()
print("Zeroing...")
orient.gyro_accel_zero()
print("Filter starting...")
orient.filter_begin_tracking(0.02)

while True:
    sleep(5)
