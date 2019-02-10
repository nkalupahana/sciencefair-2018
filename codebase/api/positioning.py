# See http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/

from gps3 import agps3

def getLatLng(self):
    gps_socket = agps3.GPSDSocket()
    data_stream = agps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print('Altitude = ', data_stream.alt)
            print('Latitude = ', data_stream.lat)

            if data_stream.lat != "n/a":
                return {'lat': round(float(data_stream.lat), 4),
                    'lng': round(float(data_stream.lon), 4)}
