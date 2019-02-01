# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep

class Positioning:
    def __init__(self):
        self.glock = gps(mode=WATCH_ENABLE) # starts info stream

    def _pull(self):
        self.glock.next()

        while self.glock.fix.latitude == 0.0:
            self.glock.next()
            sleep(0.25)

        return

    def getLatLng(self):
        self._pull()
        return {"lat": round(self.glock.fix.latitude, 4), "lng": round(self.glock.fix.longitude, 4)}

    def getAltitude(self):
        self._pull()
        return self.glock.fix.altitude

    def getGPSGroundSpeed(self):
        self._pull()
        return self.glock.fix.speed
