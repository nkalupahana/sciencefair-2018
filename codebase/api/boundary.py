from database import *
from globals import DEBUG

# currently only supports 4 points (rectangle), robot must start at first point going towards second point

# Boundary Operations
class Boundary:
    # Create database and get points
    def __init__(self, name):
        self.db = Database(name)
        _points = self.db.getPoints()

        self.points = []

        for _index, point in enumerate(_points):
            self.points.append(point)

    # Checks if robot is on boundary of drive box
    def on_boundary(self, loc, startloc):
        print("--------") if DEBUG else 0
        for index, point in enumerate(self.points):
            # Drop left line of boundary
            if index == 1:
                continue

            backindex = -10

            # Get index of point before current point
            if index == 0:
                backindex = 3
            else:
                backindex = index - 1

            # If position in latitude range of point and previous point:
            if loc["lat"] >= lower(self.points[backindex][1], self.points[index][1]) and loc["lat"] <= higher(self.points[backindex][1], self.points[index][1]):
                # If position in longitude range of point and previous point:
                if loc["lng"] >= lower(self.points[backindex][2], self.points[index][2]) and loc["lng"] <= higher(self.points[backindex][2], self.points[index][2]):
                    # If point on line between point and previous point:
                    if abs(((loc["lat"] - self.points[backindex][1]) / (self.points[index][1] - self.points[backindex][1])) - ((loc["lng"] - self.points[backindex][2]) / (self.points[index][2] - self.points[backindex][2]))) < 0.1:
                        return True


            # Debug prints
            print("Point + " str(index)) if DEBUG else 0
            print("Latitude in range : " + str(loc["lat"] >= lower(self.points[backindex][1], self.points[index][1])
                                               and loc["lat"] <= higher(self.points[backindex][1], self.points[index][1]))) if DEBUG else 0
            print("Longitude in range : " + str(loc["lng"] >= lower(self.points[backindex][2], self.points[index]
                                                                    [2]) and loc["lng"] <= higher(self.points[backindex][2], self.points[index][2]))) if DEBUG else 0
            print("At point on line : " + str(abs((((loc["lat"] - self.points[backindex][1]) / (self.points[index][1] - self.points[backindex][1])) - (
                (loc["lng"] - self.points[backindex][2]) / (self.points[index][2] - self.points[backindex][2])))))) if DEBUG else 0

        return False

    # Checks if robot has converged at top right point of boundary
    def converged(self, loc):
        if abs(loc["lat"] - self.points[2][1]) < 0.001:
            if abs(loc["lng"] - self.points[2][2]) < 0.001:
                return True

        return False

# Returns lower value
def lower(one, two):
    if one < two:
        return one
    else:
        return two

# Returns higher value
def higher(one, two):
    if one < two:
        return two
    else:
        return one
