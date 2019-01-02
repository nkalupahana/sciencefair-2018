from motors import *
from globals import *
from ninedof import *

from time import sleep
import atexit, multiprocessing
atexit.register(turnOffMotors)

class GyroDrive:
    def __init__(self, m1, m2):
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.ds = DriveSystem(mh.getMotor(m1), mh.getMotor(m2))
        self.orient = NineDOF()
        self.rightTurn = True

    def getHAT(self):
        return self.mh

    def getDriveSystem(self):
        return self.ds

    def turn_sequence(self):
        self.ds.stop()

        self.m_turn(90) if self.rightTurn else self.m_turn(-90)
        self.ds.run(100)
        sleep(1)
        self.ds.stop()
        self.m_turn(90) if self.rightTurn else self.m_turn(-90)

        self.rightTurn = not self.rightTurn

    def m_turn(self, angle):
        self.start_head = self.orient.magnometer_heading()
        self.ds.go(0, True)

        while abs((self.start_head + angle) - self.orient.magnometer_heading()) > 0.1:
            error = (self.start_head + angle) - self.orient.magnometer_heading()
            self.ds.adjustSpeed(error * 20)
            sleep(0.05)

        self.ds.stop()

    def ga_turn(self, angle):
        self.orient.gyro_accel_heading_begin_tracking(0.05)
        self.ds.go(0, True)

        while abs(orient.gyro_accel_heading() - angle) > 0.1:
            error = orient.gyro_accel_heading() - angle
            self.ds.adjustSpeed(error * 20)
            sleep(0.05)

        self.orient.gyro_accel_heading_terminate()
        self.ds.stop()

    def c_turn(self, angle):
        self.orient.comb_heading_begin_tracking(0.05)
        self.ds.go(0, True)

        while abs(orient.gyro_accel_heading() - angle) > 0.1:
            error = orient.gyro_accel_heading() - angle
            self.ds.adjustSpeed(error * 20)
            sleep(0.05)

        self.orient.comb_heading_terminate()


    def straight_drive_start(self, speed):
        self.ds.go(speed)

        # Magnometer:
        self.start_head = self.orient.magnometer_heading()

        # Gyro/Accelerometer:
        #self.orient.gyro_accel_heading_begin_tracking(0.1)

        # Combined:
        #self.orient.comb_heading_begin_tracking(0.1)

        self.heading_thread = multiprocessing.Process(target=self._thread_straight_drive_m) # or _thread_straight_drive_ga_c
        self.heading_thread.daemon = True
        self.heading_thread.start()


    def straight_drive_terminate(self):
        self.ds.stop()
        self.heading_thread.terminate()
        self.heading_thread = None

        try:
            self.orient.gyro_accel_heading_terminate()
        except:
            pass

        try:
            self.orient.comb_heading_terminate()
        except:
            pass

    def _thread_straight_drive_m(self):
        while True:
            error = self.start_head - self.orient.magnometer_heading()
            self.ds.adjustSpeed(error * 8)
            sleep(0.1)

    def _thread_straight_drive_ga_c(self):
        while True:
            error = self.orient.gyro_accel_heading()
            self.ds.adjustSpeed(error * 8)
            sleep(0.1)
