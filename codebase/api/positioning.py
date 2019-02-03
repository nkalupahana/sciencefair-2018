# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy

class Positioning:
    def __init__(self):
        self.glock = gps(mode=WATCH_ENABLE) # starts info stream

    def _pull(self):
        self.glock.fix = None
        self.glock.next()

        while self.glock.fix == None:
            print("waiting")
            self.glock.next()
            sleep(0.25)

        while self.glock.fix.latitude == 0.0:
            print("waiting")
            self.glock.next()
            sleep(0.25)

        while self.glock.fix.longitude == 0.0:
            self.glock.next()
            sleep(0.25)

        sleep(1)
        print("out")

        return

    def getLatLng(self):
        self._pull()
        print("okay")
        return {"lat": round(self.glock.fix.latitude, 5), "lng": round(self.glock.fix.longitude, 5)}

    def getAltitude(self):
        self._pull()
        return self.glock.fix.altitude

    def getGPSGroundSpeed(self):
        self._pull()
        return self.glock.fix.speed
