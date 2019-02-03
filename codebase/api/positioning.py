# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy

class Positioning:
    def __init__(self):
        self.glock = gps(mode=WATCH_ENABLE) # starts info stream

    def _pull(self):
        track = copy.deepcopy(self.glock.fix.track)
        print(track)
        self.glock.next()

        while self.glock.fix.latitude == 0.0:
            self.glock.next()
            sleep(0.25)

        while self.glock.fix.track == track:
            print("SAME")
            self.glock.next()
            sleep(0.5)

        print(self.glock.fix.track)
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
