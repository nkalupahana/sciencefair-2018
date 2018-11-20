# https://raspberrypi.stackexchange.com/questions/30170/piezo-with-python

import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

c = 261
d = 294
e = 329
f = 349
g = 392
a = 440
b = 493
C = 423
r = 1
p = GPIO.PWM(15, 100)
def Blink(numTimes, speed):
    for i in range(0,numTimes):
        print "Iteration " + str(i+1)
        GPIO.output(7, True)
        GPIO.output(15, True)
        time.sleep(speed) ## Wait
        p.start(100)             # start the PWM on 100  percent duty cycle
        p.ChangeDutyCycle(90)   # change the duty cycle to 90%
        p.ChangeFrequency(c)  # change the frequency to 261 Hz (floats also work)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(d)  # change the frequency to 294 Hz (floats also work)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(e)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(f)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(g)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(a)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(b)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(C)
        time.sleep(speed) ## Wait
        p.ChangeFrequency(r)
        time.sleep(speed) ## Wait
        p.stop()                # stop the PWM output

    print "Done" ## When loop is complete, print "Done"
    GPIO.cleanup()

iterations = 4
speed = 2

Blink(int(iterations),float(speed))
