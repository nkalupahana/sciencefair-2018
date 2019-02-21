from motors import *
from globals import *
from ninedof import *

from time import sleep
import atexit
import multiprocessing
from multiprocessing import Queue
from globals import DEBUG

class GyroDrive:
    def __init__(self, m1, m2):
        # Forces motors to stop on unclean exit
        atexit.register(turnOffMotors)
        
        # Initialize lower-level drive
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.ds = DriveSystem(self.mh.getMotor(m1), self.mh.getMotor(m2))

    # Get HAT instance
    def getHAT(self):
        return self.mh

    # Get DriveSystem instance
    def getDriveSystem(self):
        return self.ds

    # Turn, forward a little, turn back
    def turn_sequence(self, flip):
        # Stop drive (important for gyro/accel zero)
        self.ds.stop()
        sleep(1)
        # Turn 90 degrees (scales to 65)
        self.ga_turn(65) if flip else self.ga_turn(-65)
        sleep(1)
        # Forward a bit (advances robot to next strip of lawn)
        self.ds.go(100)
        sleep(2)
        self.ds.stop()
        sleep(1)
        # Turn back 90 degrees (scales to 65)
        self.ga_turn(65) if flip else self.ga_turn(-65)
        sleep(1)

    # Gyro/Accelerometer turn subroutine
    def ga_turn(self, angle):
        # Create gyro/accel instance and queue for data access
        orient = NineDOF()
        q = Queue()

        # Zero accel and gyro
        orient.gyro_accel_zero()
        sleep(1)
        # Begin tracking -- send data to q every 0.01 seconds
        orient.ga_heading_begin_tracking(0.01, q)

        # Stall drive
        self.ds.go(0, True)

        # If angle is positive:
        if angle > 0:
            # Set motor direction accordingly
            self.ds.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.ds.m2.run(Adafruit_MotorHAT.FORWARD)

            # While over 10 degrees of error, turn somewhat quickly
            while abs(q.get() + angle) > 10:
                error = q.get() + angle
                print(error) if DEBUG else 0
                self.ds._setSpeed(90)

            # Then, turn more slowly to the specified angle
            while abs(q.get() + angle) > 0.25:
                error = q.get() + angle
                print(error) if DEBUG else 0
                self.ds._setSpeed(70)
        else:
            # Set motor direction accordingly
            self.ds.m1.run(Adafruit_MotorHAT.FORWARD)
            self.ds.m2.run(Adafruit_MotorHAT.BACKWARD)

            # While over 10 degrees of error, turn somewhat quickly
            while abs(q.get() + angle) > 10:
                error = q.get() + angle
                print(error) if DEBUG else 0
                self.ds._setSpeed(90)

            # Then, turn more slowly to the specified angle
            while abs(q.get() + angle) > 0.25:
                error = q.get() + angle
                print(error) if DEBUG else 0
                self.ds._setSpeed(70)

        # Stop everything
        orient.ga_heading_terminate()
        self.ds.stop()

    # Start straight drive thread
    def straight_drive_start(self, speed):
        self.ds.stop()

        self.heading_thread = multiprocessing.Process(
            target=self._thread_straight_drive_ga, args=(speed, ))
        self.heading_thread.daemon = False
        self.heading_thread.start()

    # Terminate straight drive thread
    def straight_drive_terminate(self):
        self.ds.stop()
        self.heading_thread.terminate()
        self.heading_thread = None

    def _thread_straight_drive_ga(self, speed):
        # Create gyro/accel instance and queue for data access
        orient = NineDOF()
        q = Queue()

        # Zero accel and gyro
        orient.gyro_accel_zero()
        sleep(1)
        # Begin tracking -- send data to q every 0.01 seconds
        orient.ga_heading_begin_tracking(0.01, q)

        self.ds.go(speed)

        # Empty data queue
        while True:
            while not q.empty():
                try:
                    q.get(False)
                except Empty:
                    continue

            # Get error
            error = q.get()
            print(error) if DEBUG else 0
            # Adjust motor speed based on angle error (adds to right, subtracts from left)
            self.ds.adjustSpeed(int(round(error * -10, 0)))
            sleep(0.25)
