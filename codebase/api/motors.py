from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from time import sleep

# Function to be passed into atexit to stop motors on unclean program exit
def turnOffMotors():
    mh = Adafruit_MotorHAT(addr=0x60)
    mh.getMotor(1).setSpeed(0)
    mh.getMotor(2).setSpeed(0)
    mh.getMotor(3).setSpeed(0)
    mh.getMotor(4).setSpeed(0)
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Cutter motor control
class Cutter:
    def __init__(self, motor):
        self.cutter = motor

    # Runs cutter
    def cut(self):
        self.cutter.setSpeed(255)
        self.cutter.run(Adafruit_MotorHAT.FORWARD)
        sleep(4)
        self.cutter.setSpeed(0)
        self.cutter.run(Adafruit_MotorHAT.RELEASE)

# Base drive control
class DriveSystem:
    def __init__(self, motor1, motor2):
        self.m1 = motor1
        self.m2 = motor2

    # Adjusts base motor speed (add to right, subtract from left)
    def adjustSpeed(self, adj):
        # Speed adjustment for left motor
        if (self.currentSpeed + adj) >= 0:
            self.m1.run(Adafruit_MotorHAT.FORWARD)
            self.m1.setSpeed(self.currentSpeed + adj)
        else:
            self.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.m1.setSpeed(abs(self.currentSpeed + adj))

        # Speed adjustment for right motor
        if (self.currentSpeed - adj) >= 0:
            self.m2.run(Adafruit_MotorHAT.FORWARD)
            self.m2.setSpeed(self.currentSpeed - adj)
        else:
            self.m2.run(Adafruit_MotorHAT.BACKWARD)
            self.m2.setSpeed(abs(self.currentSpeed - adj))

    # Base drive base speed set function (no checks)
    def _setSpeed(self, speed):
        self.currentSpeed = speed
        self.m1.setSpeed(speed)
        self.m2.setSpeed(speed)

    # Base drive speed set function (with checks)
    def go(self, speed, override=False):
        if speed == 0 and not override:
            raise ValueError('You shouldn\'t be setting speed to 0! Call' +
                             ' .stop() instead!')

        # Set direction and speed
        if speed >= 0:
            self.m1.run(Adafruit_MotorHAT.FORWARD)
            self.m2.run(Adafruit_MotorHAT.FORWARD)
            self._setSpeed(speed)
        else:
            self.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.m2.run(Adafruit_MotorHAT.BACKWARD)
            self._setSpeed(-speed)

    # Stop drive base motors
    def stop(self):
        self._setSpeed(0)
        self.m1.run(Adafruit_MotorHAT.RELEASE)
        self.m2.run(Adafruit_MotorHAT.RELEASE)
