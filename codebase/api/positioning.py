# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps3.agps3threaded import AGPS3mechanism

class Positioning:
    def __init__(self):
        self.agps_thread = AGPS3mechanism()
        self.agps_thread.stream_data()
        self.agps_thread.run_thread()
        return

    def getLatLng(self):
        print(self.agps_thread.data_stream.lat)
        return {'lat': round(float(self.agps_thread.data_stream.lat), 4),
            'lng': round(float(self.agps_thread.data_stream.lon), 4)}
