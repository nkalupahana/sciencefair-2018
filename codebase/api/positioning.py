# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

import os
from gps import *
from time import sleep
import threading

glock = None #seting the global variable

def gpssystem():
    global glock
    glock = gps(mode=WATCH_ENABLE) # starting the stream of info

    while True:
      glock.next() # this will continue to loop and grab EACH set of gpsd info to clear the buffer


"""

Here's a test script/attributes (gpsd == glock):

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try
    gpsp.start() # start it up
    while True:
      # It may take a second or two to get good data
      os.system('clear')

      print
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      print 'sats        ' , gpsd.satellites

      sleep(5) # set to whatever
"""
