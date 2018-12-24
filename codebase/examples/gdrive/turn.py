import sys
sys.path.append("../../")

from api.gyrodrive import *
from time import sleep

gdrive = GyroDrive()
gdrive.m_turn(90)
sleep(1)
gdrive.ga_turn(-90)
