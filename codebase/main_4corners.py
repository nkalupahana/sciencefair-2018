#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys, multiprocessing
sys.path.append("../../")
sys.path.append("../../api")
from api import *
from Adafruit_MotorHAT import *

atexit.register(motors.turnOffMotors)

# system component initialization
#drive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
#cutter = Cutter(drive.getHAT().getMotor(CUTTER_MOTOR))
#camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
ds = motors.DriveSystem(mh.getMotor(m1), mh.getMotor(m2))positioning = positioning.Positioning()
startloc = positioning.getLatLng()
bounds = boundary.Boundary(globals.DATABASE_NAME)

# Start main driver system thread
dt = multiprocessing.Process(target=_driver)
dt.daemon = True
dt.start()

def _driver():
    #drive.straight_drive_start(100)


    while not bounds.converged(positioning.getLatLng, startloc):
        if bounds.on_boundary():
            drive.straight_drive_terminate()
            print("DONE")
            #drive.turn_sequence()

        """

        ymin = camera.run()
        if (camera.run() != 0):
            sleep(ymin / 40)
            drive.getDriveSystem().go(50)
            cutter.cut()
            drive.getDriveSystem().go(-10) # Wait for further camera input
        else:
            drive.getDriveSystem().go(100)

        drive.getDriveSystem().stop()
        """
