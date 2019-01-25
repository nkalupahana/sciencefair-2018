import sys
sys.path.append("../../")
sys.path.append("../../api")

from time import sleep
from api.ninedof import *

orient = NineDOF()
orient.filter_begin_tracking(0.02)

while True:
    sleep(5)
