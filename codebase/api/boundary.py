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
        for line in self.lines:
            # If in x range:
            if 0 <= ((loc["lat"] - line["xint"]) / line["xslope"]) <= 1:
                # If in y range:
                if 0 <= ((loc["lng"] - line["yint"]) / line["yslope"]) <= 1:
                    # If at point on line:
                    if (((loc["lng"] - line["yint"]) / line["yslope"]) - ((loc["lat"] - line["xint"]) / line["xslope"])) < 0.01:
                        # If not at starting point
                        if loc != startloc:
                            return True

            print("X v. Slope: " + str((loc.lat - line.xint) / line.xslope))
            print("Y v. Slope: " + str((loc.lng - line.yint) / line.yslope))

        return False

    def converged(self, loc):
        line = self.lines[1]

        # If at right x end:
        if 0 == ((loc["lat"] - line["xint"]) / line["xslope"]):
            # If at right y end:
            if 0 == ((loc["lng"] - line["yint"]) / line["yslope"]):
                return True

        return False
