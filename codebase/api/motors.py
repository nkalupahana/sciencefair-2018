def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)

class Cutter:
    def __init__(motor):
        self.cutter = motor

    def cut():
        self.cutter.setSpeed(255)
        self.cutter.run(Adafruit_MotorHAT.FORWARD)
        sleep(4)
        self.cutter.run(Adafruit_MotorHAT.RELEASE)


class DriveSystem:
    def __init__(motor1, motor2):
        self.m1 = motor1
        self.m2 = motor2

    def setSpeed(speed):
        self.m1.setSpeed(speed)
        self.m2.setSpeed(speed)

    def start(speed):
        if speed:
            self.m1.setSpeed(speed)
            self.m2.setSpeed(speed)

        if speed == 0:
            raise ValueError('You shouldn\'t be setting speed to 0! Call' +
            ' .stop() instead!')

        self.m1.run(Adafruit_MotorHAT.FORWARD)
        self.m2.run(Adafruit_MotorHAT.FORWARD)

    def stop():
        self.m1.run(Adafruit_MotorHAT.RELEASE)
        self.m2.run(Adafruit_MotorHAT.RELEASE)
