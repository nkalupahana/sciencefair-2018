import sys
sys.path.append("../../")
sys.path.append("../../api")

from api.gyrodrive import *
from api.globals import *
from time import sleep

gdrive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
gdrive.straight_drive_start(100)
sleep(15)
gdrive.straight_drive_terminate()
