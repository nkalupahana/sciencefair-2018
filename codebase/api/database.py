import sqlite3

class Database:
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.dbc = self.db.cursor()

    def prepare(self):
        try:
            self.dbc.execute("DROP TABLE POINTS")
        except:
            pass

        self.dbc.execute("CREATE TABLE POINTS (lat NUMERIC, lng NUMBERIC)")
        return

    def put(self, lat, lng):
        self.dbc.execute("INSERT INTO POINTS values(" + str(lat) + ", " + str(lng) + ")")
        self.db.commit()
        return

    def getPoints(self):
        return self.db.execute("SELECT * FROM POINTS")
