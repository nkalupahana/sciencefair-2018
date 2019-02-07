from database import *

# currently only supports 4 self.points (rectangle), robot must start at first point going towards second point
class Boundary:
    def __init__(self, name):
        self.db = Database(name)
        _points = self.db.getPoints()

        self.points = [];

        for _index, point in enumerate(_points):
            self.points.append(point)

    def on_boundary(self, loc, startloc):
        print("--------")
        for index, point in enumerate(self.points):
            if index == 1:
                continue

            backindex = -10

            if index == 0:
                backindex = 3
            else:
                backindex = index - 1

            if loc["lat"] >= lower(self.points[backindex][1], self.points[index][1]) and loc["lat"] <= higher(self.points[backindex][1], self.points[index][1]):
                if loc["lng"] >= lower(self.points[backindex][2], self.points[index][2]) and loc["lng"] <= higher(self.points[backindex][2], self.points[index][2]):
                    if abs(((loc["lat"] - self.points[backindex][1]) / (self.points[index][1] - self.points[backindex][1])) - ((loc["lng"] - self.points[backindex][2]) / (self.points[index][2] - self.points[backindex][2]))) < 0.1:
                        return True

            print("Point + " str(index))
            print("Latitude in range : " + str(loc["lat"] >= lower(self.points[backindex][1], self.points[index][1]) and loc["lat"] <= higher(self.points[backindex][1], self.points[index][1])))
            print("Longitude in range : " + str(loc["lng"] >= lower(self.points[backindex][2], self.points[index][2]) and loc["lng"] <= higher(self.points[backindex][2], self.points[index][2])))
            print("At point on line : " + str(abs((((loc["lat"] - self.points[backindex][1]) / (self.points[index][1] - self.points[backindex][1])) - ((loc["lng"] - self.points[backindex][2]) / (self.points[index][2] - self.points[backindex][2]))))))

        return False

    def converged(self, loc):
        if abs(loc["lat"] - self.points[2][1]) < 0.001:
            if abs(loc["lng"] - self.points[2][2]) < 0.001:
                return True

        return False

def lower(one, two):
    if one < two:
        return one
    else:
        return two

def higher(one, two):
    if one < two:
        return two
    else:
        return one
