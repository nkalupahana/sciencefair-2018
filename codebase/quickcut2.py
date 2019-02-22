from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import sys
sys.path.append("./")
sys.path.append("./api")

from api.motors import *
from api.globals import *
from api.camera import *

# Initialize components
camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
cutter = Cutter(mh.getMotor(3))

ds.go(75)

while True:
    ymin = camera.run()                    # Move network forward
    if (ymin != -1):                       # If bounding box found
        sleep(ymin)                        # Sleep until on top of weed
        ds.go(40)
        cutter.cut()
        ds.go(-10)                         # Stall until checks are run again
    else:
        ds.go(75)
