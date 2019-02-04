from database import *

# currently only supports 4 points (rectangle), robot must start in bottom left corner
class Boundary:
    def __init__(self, name):
        self.db = Database(name)
        _points = self.db.getPoints()

        self.lines = {"xslope": [], "xint": [], "yslope": [], "yint": []}

        points = [];

        for _index, point in enumerate(_points):
            points.append(point)

        for index, point in enumerate(points):
            if index == 1:
                continue

            backindex = -10

            if index == 0:
                backindex = 0
            else:
                backindex = index - 1

            self.lines["xslope"].append(point[1] - points[backindex][1])
            self.lines["yslope"].append(point[2] - points[backindex][2])
            self.lines["xint"].append(points[backindex][1])
            self.lines["yint"].append(points[backindex][2])

    def on_boundary(self, loc, startloc):
        print("--------")
        for i, _f in enumerate(self.lines.xint):
            # If in x range:
            if 0 <= ((loc["lat"] - self.lines["xint"][i]) / self.lines["xslope"][i]) <= 1:
                # If in y range:
                if 0 <= ((loc["lng"] - self.lines["yint"][i]) / self.lines["yslope"][i]) <= 1:
                    # If at point on line:
                    if abs(((loc["lng"] - self.lines["yint"][i]) / self.lines["yslope"][i]) - ((loc["lat"] - self.lines["xint"][i]) / self.lines["xslope"][i])) < 0.01:
                        # If not at starting point
                        if loc != startloc:
                            return True

            print("X v. Slope: " + str((loc["lat"] - self.lines["xint"][i]) / self.lines["xslope"][i]))
            print("Y v. Slope: " + str((loc["lng"] - self.lines["yint"][i]) / self.lines["yslope"][i]))

        return False

    def converged(self, loc):
        i = 1

        # If at right x end:
        if -0.01 < ((loc["lat"] - self.lines["xint"][i]) / self.lines["xslope"][i]) < 0.01:
            # If at right y end:
            if -0.01 < ((loc["lng"] - self.lines["yint"][i]) / self.lines["yslope"][i]) < 0.01:
                return True

        return False
