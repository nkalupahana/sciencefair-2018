import sys
sys.path.append("../../")

from time import sleep
from api.ninedof import *

orient = NineDOF()
orient.gyro_heading_begin_tracking(0.1)

while True:
    print(orient.get_heading())
    sleep(0.1)
