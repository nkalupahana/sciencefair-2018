#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit, sys
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
camera = Camera(GRAPH_PATH, DETECTION_LIMIT, IOU_LIMIT, LABELS)
mh = Adafruit_MotorHAT(addr=0x60)
ds = DriveSystem(mh.getMotor(1), mh.getMotor(2))
cutter = Cutter(ds.getMotor(CUTTER_MOTOR))
q = Queue()
positioning = Positioning(q)
sleep(5)

def emptyQueue():
    global q
    while not q.empty():
        try:
            q.get(False)
        except Empty:
            continue

emptyQueue()
startloc = q.get()
bounds = Boundary(DATABASE_NAME)
print("START")
print(startloc)

def getLatLng():
    val = q.get()
    print(val)
    return val

ds.go(100)

while True:
    emptyQueue()
    loc = getLatLng()
    if bounds.converged(loc):
        break

    if bounds.on_boundary(loc, startloc):
        print("DONE")
        ds.stop()
        #drive.straight_drive_terminate()
        #drive.turn_sequence()


    ymin = camera.run()
    if (ymin != 0):
        sleep(ymin + 2)
        ds.go(50)
        cutter.cut()
        ds.go(-10)
    else:
        ds.go(100)


ds.stop()
