import os
from gpspy3 import gps
from gpspy3 import *
from time import *
import time
import threading

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps.GPS(mode=gps.WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

      os.system('clear')

      print(' GPS reading')
      print('----------------------------------------')
      print('latitude    ' + str(gpsd.fix.latitude))
      print('longitude   ' + str(gpsd.fix.longitude))
      print('time utc    ' + str(gpsd.utc),' + ', str(gpsd.fix.time))
      print('altitude (m)' + str(gpsd.fix.altitude))
      print('eps         ' + str(gpsd.fix.eps))
      print('epx         ' + str(gpsd.fix.epx))
      print('epv         ' + str(gpsd.fix.epv))
      print('ept         ' + str(gpsd.fix.ept))
      print('speed (m/s) ' + str(gpsd.fix.speed))
      print('climb       ' + str(gpsd.fix.climb))
      print('track       ' + str(gpsd.fix.track))
      print('mode        ' + str(gpsd.fix.mode))
      print('')
      print('sats        ' + gpsd.satellites)

      time.sleep(1) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print('\nKilling Thread...')
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
