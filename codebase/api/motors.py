from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from time import sleep

def turnOffMotors():
    mh = Adafruit_MotorHAT(addr=0x60)
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

class Cutter:
    def __init__(self, motor):
        self.cutter = motor

    def cut(self):
        self.cutter._setSpeed(255)
        self.cutter.run(Adafruit_MotorHAT.FORWARD)
        sleep(4)
        self.cutter._setSpeed(0)
        self.cutter.run(Adafruit_MotorHAT.RELEASE)


class DriveSystem:
    def __init__(self, motor1, motor2):
        self.m1 = motor1
        self.m2 = motor2

    def _setSpeed(self, speed):
        self.m1._setSpeed(speed)
        self.m2._setSpeed(speed)

    def go(self, speed):
        if speed == 0:
            raise ValueError('You shouldn\'t be setting speed to 0! Call' +
            ' .stop() instead!')

        if speed:
            if speed > 0:
                self.m1.run(Adafruit_MotorHAT.FORWARD)
                self.m2.run(Adafruit_MotorHAT.FORWARD)
                self._setSpeed(speed)
            else:
                self.m1.run(Adafruit_MotorHAT.BACKWARD)
                self.m2.run(Adafruit_MotorHAT.BACKWARD)
                self._setSpeed(-speed)
        else:
            raise ValueError('Setting speed is required!')

    def stop(self):
        self.m1._setSpeed(0)
        self.m2._setSpeed(0)
        self.m1.run(Adafruit_MotorHAT.RELEASE)
        self.m2.run(Adafruit_MotorHAT.RELEASE)
