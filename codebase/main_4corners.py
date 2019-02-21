#!/usr/bin/python3

import sys
sys.path.append("./")
sys.path.append("./api")

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from time import sleep
from Adafruit_MotorHAT import *
from multiprocessing import Queue

from api.motors import *
from api.positioning import *
from api.boundary import *
from api.globals import *

# System component initialization
camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
gd = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
cutter = Cutter(ds.getMotor(CUTTER_MOTOR))
positioning = Positioning()

# Get starting location to ensure starting location doesn't count
# for being on boundary
startloc = positioning.getLatLng()
bounds = Boundary(DATABASE_NAME)

print("START") if DEBUG else 0
print(startloc) if DEBUG else 0

gd.straight_drive_start(100)

while True:
    loc = positioning.getLatLng()          # Get position
    if bounds.converged(loc):              # If converged, exit
        print("DONE") if DEBUG else 0
        break

    if bounds.on_boundary(loc, startloc):  # If on boundary, turn
        print("BOUNDED") if DEBUG else 0
        gd.straight_drive_terminate()
        sleep(1)
        gd.turn_sequence()
        sleep(1)
        gd.straight_drive_start()

    ymin = camera.run()                    # Move network forward
    if (ymin != -1):                       # If bounding box found
        sleep(ymin + 2)                    # Sleep until on top of weed
        ds.go(50)
        cutter.cut()
        ds.go(-10)                         # Stall until checks are run again
    else:
        ds.go(100)


gd.straight_drive_terminate()
