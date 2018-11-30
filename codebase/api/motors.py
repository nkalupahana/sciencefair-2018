from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from time import sleep

def turnOffMotors():
    mh = Adafruit_MotorHAT(addr=0x60)
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)

class Cutter:
    def __init__(self, motor):
        self.cutter = motor

    def cut(self):
        self.cutter.setSpeed(255)
        self.cutter.run(Adafruit_MotorHAT.FORWARD)
        sleep(4)
        self.cutter.setSpeed(0)
        self.cutter.run(Adafruit_MotorHAT.RELEASE)


class DriveSystem:
    def __init__(self, motor1, motor2):
        self.m1 = motor1
        self.m2 = motor2

    def setSpeed(self, speed):
        if speed > 0:
            self.m1.run(Adafruit_MotorHAT.FORWARD)
            self.m2.run(Adafruit_MotorHAT.FORWARD)
        else:
            self.m1.run(Adafruit_MotorHAT.BACKWARD)
            self.m2.run(Adafruit_MotorHAT.BACKWARD)

        self.m1.setSpeed(speed)
        self.m2.setSpeed(speed)

    def start(self, speed):
        if speed:
            if speed > 0:
                self.m1.run(Adafruit_MotorHAT.FORWARD)
                self.m2.run(Adafruit_MotorHAT.FORWARD)
                self.setSpeed(speed)
            else:
                self.m1.run(Adafruit_MotorHAT.BACKWARD)
                self.m2.run(Adafruit_MotorHAT.BACKWARD)
                self.setSpeed(-speed)

        if speed == 0:
            raise ValueError('You shouldn\'t be setting speed to 0! Call' +
            ' .stop() instead!')

        self.m1.run(Adafruit_MotorHAT.FORWARD)
        self.m2.run(Adafruit_MotorHAT.FORWARD)

    def stop(self):
        self.m1.setSpeed(0)
        self.m2.setSpeed(0)
        self.m1.run(Adafruit_MotorHAT.RELEASE)
        self.m2.run(Adafruit_MotorHAT.RELEASE)
