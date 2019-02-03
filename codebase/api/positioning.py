# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps import *
from time import sleep
import copy
import threading

class Positioning:
    def __init__(self, q):
        start_gps_thread(q)
        return

    def start_gps_thread(self, q):
        self.gyro_thread = multiprocessing.Process(target=self._thread_gps, args=(q, ))
        self.gyro_thread.daemon = True
        self.gyro_thread.start()

    def _thread_gps(self, q):
        gpsd = gps(mode=WATCH_ENABLE)

        while True:
            gpsd.next()
            sleep(1)
            q.put({"lat": gpsd.fix.latitude, "lng": gpsd.fix.latitude})
