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
        sleep(1)
        self.ga_turn(65) if flip else self.ga_turn(-65)
        sleep(1)
        self.ds.run(100)
        sleep(2)
        self.ds.stop()
        self.ga_turn(65) if flip else self.ga_turn(-65)
        sleep(1)

    def ga_turn(self, angle):
        orient = NineDOF()
        q = Queue()

        orient.gyro_accel_zero()
        sleep(1)
        orient.ga_heading_begin_tracking(0.01, q)

        self.ds.go(0, True)

        if angle > 0:
            self.ds.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.ds.m2.run(Adafruit_MotorHAT.FORWARD)

            while abs(q.get() + angle) > 10:
                error = q.get() + angle
                print(error)
                self.ds._setSpeed(90)

            while abs(q.get() + angle) > 0.25:
                error = q.get() + angle
                print(error)
                self.ds._setSpeed(70)
        else:
            self.ds.m1.run(Adafruit_MotorHAT.FORWARD)
            self.ds.m2.run(Adafruit_MotorHAT.BACKWARD)

            while abs(q.get() + angle) > 10:
                error = q.get() + angle
                print(error)
                self.ds._setSpeed(90)

            while abs(q.get() + angle) > 0.25:
                error = q.get() + angle
                print(error)
                self.ds._setSpeed(70)

        orient.ga_heading_terminate()
        self.ds.stop()

    def straight_drive_start(self, speed):
        self.ds.stop()

        self.heading_thread = multiprocessing.Process(target=self._thread_straight_drive_ga, args=(speed, ))
        self.heading_thread.daemon = False
        self.heading_thread.start()

    def straight_drive_terminate(self):
        self.ds.stop()
        self.heading_thread.terminate()
        self.heading_thread = None

    def _thread_straight_drive_ga(self, speed):
        orient = NineDOF()
        q = Queue()

        orient.gyro_accel_zero()
        sleep(1)
        orient.ga_heading_begin_tracking(0.01, q)

        self.ds.go(speed)

        while True:
            error = q.get()
            print(error)
            self.ds.adjustSpeed(int(error * 10))
            sleep(0.1)
