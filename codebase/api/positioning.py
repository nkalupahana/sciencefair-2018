# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy
import threading
import multiprocessing

class Positioning:
    def __init__(self, q):
        self.start_gps_thread(q)
        return

    def start_gps_thread(self, q):
        self.thrd = multiprocessing.Process(target=self._thread_gps, args=(q, ))
        self.thrd.daemon = True
        self.thrd.start()

    def _thread_gps(self, q):
        gpsd = gps(mode=WATCH_ENABLE)

        while True:
            gpsd.next()
            sleep(1)
            q.put({"lat": round(gpsd.fix.latitude, 5), "lng": round(gpsd.fix.longitude, 5)})
