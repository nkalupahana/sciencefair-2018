#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys, multiprocessing
sys.path.append("../../")
sys.path.append("../../api")
from Adafruit_MotorHAT import *
from multiprocessing import Queue
from api.motors import *
from api.positioning import *
from api.boundary import *
from api.globals import *

atexit.register(turnOffMotors)

# system component initialization
#drive = GyroDrive(BASE_MOTOR_1, BASE_MOTOR_2)
#cutter = Cutter(drive.getHAT().getMotor(CUTTER_MOTOR))
#camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
q = Queue()
positioning = Positioning(q)
sleep(5)
while not q.empty():
    try:
        q.get(False)
    except Empty:
        continue

startloc = q.get()
bounds = Boundary(DATABASE_NAME)
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
