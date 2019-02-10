import sys
sys.path.append("../../")
sys.path.append("../../api")

from api.gyrodrive import *
from api.globals import *
from time import sleep

gdrive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
gdrive.ga_turn(-62)
sleep(5)
gdrive.ga_turn(62)

#sleep(5)
#gdrive.ga_turn(90)
#gdrive.c_turn(90)
