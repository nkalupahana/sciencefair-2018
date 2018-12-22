# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *

class Positioning:
    def __init__(self):
        self.glock = gps(mode=WATCH_ENABLE) # starts info stream

    def _pull(self):
        glock.next()
        return

    def getLatLng(self):
        self._pull()
        return {lat: glock.fix.latitude, lng: glock.fix.longitude}

    def getAltitude(self):
        self._pull()
        return glock.fix.altitude

    def getGPSGroundSpeed(self):
        self._pull()
        return glock.fix.speed
