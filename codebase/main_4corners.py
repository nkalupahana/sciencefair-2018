#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys, multiprocessing
sys.path.append("../../")
sys.path.append("../../api")
from api import *
from Adafruit_MotorHAT import *
from multiprocessing import Queue

atexit.register(motors.turnOffMotors)

# system component initialization
#drive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
#cutter = Cutter(drive.getHAT().getMotor(CUTTER_MOTOR))
#camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
ds = motors.DriveSystem(mh.getMotor(m1), mh.getMotor(m2))
q = Queue()
positioning = positioning.Positioning(q)
sleep(5)
while not q.empty():
    try:
        q.get(False)
    except Empty:
        continue

startloc = q.get()
bounds = boundary.Boundary(globals.DATABASE_NAME)
print("START")
print(startloc)

# Start main driver system thread
dt = multiprocessing.Process(target=_driver)
dt.daemon = True
dt.start()

def getLatLng():
    val = q.get()
    print(val)
    return val

def _driver():
    ds.go(100)

    while not bounds.converged(getLatLng, startloc):
        if bounds.on_boundary():
            print("DONE")
            ds.stop()
            #drive.straight_drive_terminate()
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
