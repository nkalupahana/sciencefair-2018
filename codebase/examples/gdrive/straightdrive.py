import sys
sys.path.append("../../")

from api.gyrodrive import *
from time import sleep

gdrive = GyroDrive()
gdrive.straight_drive_start(100)
sleep(15)
gdrive.straight_drive_terminate()