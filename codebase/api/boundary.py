from database import *

# currently only supports 4 points (rectangle), robot must start in bottom left corner
class Boundary:
    def __init__(self, name):
        self.db = Database(name)
        points = self.db.getPoints()
#        if len(points) != 4:
 #           raise ValueError("You need a database of 4 points!")

        self.lines = {"xslope": [], "xint": [], "yslope": [], "yint": []}

        for index, point in enumerate(points):
            self.lines["xslope"].append(point[1] - points[index - 1][1])
            self.lines["yslope"].append(point[2] - points[index - 1][2])
            self.lines["xint"].append(points[index - 1][1])
            self.lines["yint"].append(points[index - 1][2])

    def on_boundary(self, loc):
        print("--------")
        for line in self.lines:
            # If in x range:
            if 0 <= ((loc.lat - line.xint) / line.xslope) <= 1:
                # If in y range:
                if 0 <= ((loc.lng - line.yint) / line.yslope) <= 1:
                    # If at point on line:
                    if ((loc.lat - line.xint) / line.xslope) == ((loc.lng - line.yint) / line.yslope):
                        return True

            print(((loc.lat - line.xint) / line.xslope))
            print(((loc.lng - line.yint) / line.yslope))
            print(((loc.lat - line.xint) / line.xslope) == ((loc.lng - line.yint) / line.yslope))

        return False

    def converged(self, startloc, loc):
        for line in self.lines:
            # If at x end:
            if (0 == ((loc.lat - line.xint) / line.xslope)) or (1 == ((loc.lat - line.xint) / line.xslope)):
                # If in y range:
                if (0 == ((loc.lng - line.yint) / line.yslope)) or (1 == ((loc.lng - line.yint) / line.yslope)):
                    if loc != startloc:
                        return True

        return False
