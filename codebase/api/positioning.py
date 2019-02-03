# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy

class Positioning:
    def __init__(self):
        self.glock = gps(mode=WATCH_ENABLE) # starts info stream
        self.data = {}

    def _pull(self):
        self.data = self.glock.next()
        return

    def getLatLng(self):
        self._pull()
        print("okay")
        return {"lat": round(self.data.fix.latitude, 5), "lng": round(self.data.fix.longitude, 5)}

    def getAltitude(self):
        self._pull()
        return self.data.fix.altitude

    def getGPSGroundSpeed(self):
        self._pull()
        return self.data.fix.speed
