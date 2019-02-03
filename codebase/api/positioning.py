# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy
import threading

gpsd = None

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info

    def run(self):
        global gpsd

        while True:
            gpsd.next()
            print(gpsd.fix.latitude)
            sleep(0.5)

class Positioning:
    def __init__(self):
        self.gpsthread = GpsPoller()
        self.gpsthread.start()
        return

    def getLatLng(self):
        global gpsd
        return {"lat": round(gpsd.fix.latitude, 5), "lng": round(gpsd.fix.longitude, 5)}

    def getAltitude(self):
        global gpsd
        return gpsd.fix.altidude

    def getGPSGroundSpeed(self):
        global gpsd
        return gpsd.fix.speed
