import sys
sys.path.append("../../")

from time import sleep
from api.ninedof import *

orient = NineDOF()

while True:
    print(orient.magnometer_heading())
    sleep(0.1)
