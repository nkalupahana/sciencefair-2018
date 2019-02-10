from motors import *
from globals import *
from ninedof import *

from time import sleep
import atexit, multiprocessing
from multiprocessing import Queue

atexit.register(turnOffMotors)

class GyroDrive:
    def __init__(self, m1, m2):
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.ds = DriveSystem(self.mh.getMotor(m1), self.mh.getMotor(m2))

    def getHAT(self):
        return self.mh

    def getDriveSystem(self):
        return self.ds

    def turn_sequence(self, flip):
        self.ds.stop()

        self.m_turn(55) if flip else self.m_turn(-55)
        self.ds.run(200)
        sleep(2)
        self.ds.stop()
        self.m_turn(55) if flip else self.m_turn(-55)

    def ga_turn(self, angle):
        orient = NineDOF()
        q = Queue()

        orient.gyro_accel_zero()
        orient.ga_heading_begin_tracking(0.01, q)

        if angle > 0:
            self.ds.m1.run(Adafruit_MotorHAT.FORWARD)
            self.ds.m2.run(Adafruit_MotorHAT.BACKWARD)
        else:
            self.ds.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.ds.m2.run(Adafruit_MotorHAT.FORWARD)

        self.ds.go(0, True)

        while abs(q.get() - 55) > 10:
            error = q.get() - 55
            print(error)
            self.ds.go(180)

        while abs(q.get() - 55) > 0.25:
            error = q.get() - 55
            print(error)
            self.ds.go(125)

        orient.ga_heading_terminate()
        self.ds.stop()

    def straight_drive_start(self, speed):
        self.ds.stop()

        self.ds.go(speed)
        self.orient.gyro_accel_heading_begin_tracking(0.01)

        self.heading_thread = multiprocessing.Process(target=self._thread_straight_drive_ga)
        self.heading_thread.daemon = True
        self.heading_thread.start()


    def straight_drive_terminate(self):
        self.ds.stop()
        self.heading_thread.terminate()
        self.heading_thread = None
        self.orient.gyro_accel_heading_terminate()

    def _thread_straight_drive_ga(self):
        orient = NineDOF()
        q = Queue()

        orient.gyro_accel_zero()
        orient.ga_heading_begin_tracking(0.01, q)

        while True:
            error = q.get()
            self.ds.adjustSpeed(error * 10)
            sleep(0.1)
