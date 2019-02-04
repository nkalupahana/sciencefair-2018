from database import *

# currently only supports 4 points (rectangle), robot must start in bottom left corner
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

            if loc["lat"] >= points[backindex][1] and loc["lat"] <= points[index][1]:
                if loc["lng"] >= points[backindex][2] and loc["lng"] <= points[index][2]:
                    if (((loc["lat"] - points[backindex][1]) / (points[index][1] - points[backindex][1])) - ((loc["lng"] - points[backindex][2]) / (points[index][2] - points[backindex][2]))) < 0.1:
                        return True

            print("Latitude in range : " + str(loc["lat"] >= points[backindex][1] and loc["lat"] <= points[index][1]))
            print("Longitude in range : " + str(loc["lng"] >= points[backindex][2] and loc["lng"] <= points[index][2]))
            print("At point on line : " + str((((loc["lat"] - points[backindex][1]) / (points[index][1] - points[backindex][1])) - ((loc["lng"] - points[backindex][2]) / (points[index][2] - points[backindex][2]))) < 0.1))

        return False

    def converged(self, loc):

        """
        TODO
        i = 2

        # If at right x end:
        if -0.01 < (loc["lat"] - self.points[2][i]) / self.lines["xslope"][i]) < 0.01:
            # If at right y end:
            if -0.01 < ((loc["lng"] - self.lines["yint"][i]) / self.lines["yslope"][i]) < 0.01:
                return True

        """

        return False
