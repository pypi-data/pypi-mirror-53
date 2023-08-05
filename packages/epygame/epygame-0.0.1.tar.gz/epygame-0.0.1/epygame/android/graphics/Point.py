import math

class Point:
    def __init__(self, *args):
        if len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 0:
            self.x = self.y = 0

    def set(self, *args):
        self.__init__(*args)

    def equals(self, x, y):
        return self.x == x and self.y == y

    def negate(self):
        self.x *= -1
        self.y *= -1

    def offset(self, dx, dy):
        self.x += dx
        self.y += dy


class PointF(Point):
    def __init__(self, *args):
        super().__init__(*args)

    def length(self, *args):
        r = PointF(*args)
        sum_sqr = 0
        for i, j in zip((0, 0), (r.x, r.y)):
            sum_sqr += (i-j)**2
        distance = math.sqrt(sum_sqr)
        return distance
