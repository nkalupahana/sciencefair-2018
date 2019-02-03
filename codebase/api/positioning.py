# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy
import threading

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info

    def run(self):
        while True:
            self.gpsd.next()
            sleep(0.5)

class Positioning:
    def __init__(self):
        self.gpsthread = GpsPoller()
        self.gpsthread.start()
        return

    def getLatLng(self):
        return {"lat": round(self.gpsthread.gpsd.fix.latitude, 5), "lng": round(self.gpsthread.gpsd.fix.longitude, 5)}

    def getAltitude(self):
        self._pull()
        return self.gpsthread.gpsd.fix.altitude

    def getGPSGroundSpeed(self):
        self._pull()
        return self.gpsthread.gpsd.fix.speed
