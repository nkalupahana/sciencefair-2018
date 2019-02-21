from gps3 import agps3
from globals import DEBUG

# Gets latitude / longidude coordinate pair
def getLatLng():
    gps_socket = agps3.GPSDSocket()      # Init GPS socket
    data_stream = agps3.DataStream()     # Init GPS data stream
    gps_socket.connect()                 # Connect GPS socket
    gps_socket.watch()                   # Watch for data over socket
    for new_data in gps_socket:          # On new data:
        if new_data:
            data_stream.unpack(new_data) # Unpack data into python-readable format
            print('Altitude = ', data_stream.alt) if DEBUG else 0
            print('Latitude = ', data_stream.lat) if DEBUG else 0

            if data_stream.lat != "n/a": # If GPS lock present
                return {'lat': round(float(data_stream.lat), 4),
                        'lng': round(float(data_stream.lon), 4)}
