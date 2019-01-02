#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys, multiprocessing
sys.path.append("../../")
from api import *

atexit.register(turnOffMotors)

# system component initialization
drive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
cutter = Cutter(drive.getHAT().getMotor(CUTTER_MOTOR))
camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
db = Database(DATABASE_NAME)
positioning = Positioning()
startloc = positioning.getLatLng()

# Start main driver system thread
dt = multiprocessing.Process(target=_driver)
dt.daemon = True
dt.start()

def _driver():
    drive.straight_drive_start(100)

    while not drive.converged(positioning.getLatLng, startloc):
        if drive.on_boundary():
            drive.turn_sequence()

        ymin = camera.run()
        if (camera.run() != 0):
            sleep(ymin / 40)
            drive.getDriveSystem().go(50)
            cutter.cut()
            drive.getDriveSystem().go(-10) # Wait for further camera input
        else:
            drive.getDriveSystem().go(100)

        drive.getDriveSystem().stop()
