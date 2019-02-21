import sqlite3
from globals import DEBUG

# Database access wrapper (database for storing path coordinates)
class Database:
    def __init__(self, name):
        # Connects to databse, gets access cursor
        self.db = sqlite3.connect(name)
        self.dbc = self.db.cursor()

    # Resets the points table
    def prepare(self):
        try:
            self.dbc.execute("DROP TABLE points")
        except:
            pass

        self.dbc.execute("CREATE TABLE points (lat NUMERIC, lng NUMBERIC)")
        return

    # Puts lat/lng point into database
    def put(self, lat, lng):
        self.dbc.execute("INSERT INTO points values(" +
                         str(lat) + ", " + str(lng) + ")")
        self.db.commit()
        print("Commited!") if DEBUG else 0
        return

    # Returns points in database
    def getPoints(self):
        return self.db.execute("SELECT rowid, lat, lng FROM points")
