import sqlite3

class Database:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.dbc = self.db.cursor()

    def prepare(self):
        try:
            self.dbc.execute("DROP TABLE points")
        except:
            pass

        self.dbc.execute("CREATE TABLE points (lat NUMERIC, lng NUMBERIC)")
        return

    def put(self, lat, lng):
        self.dbc.execute("INSERT INTO points values(" + str(lat) + ", " + str(lng) + ")")
        self.db.commit()
        print("Commited!")
        return

    def getPoints(self):
        return self.db.execute("SELECT rowid, lat, lng FROM points")
