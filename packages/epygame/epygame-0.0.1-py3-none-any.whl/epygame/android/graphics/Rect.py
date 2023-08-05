import math
from .Point import Point, PointF

class Rect:
    def __init__(self, *args):
        if len(args) == 1:
            rect = args[0]
            self.left = rect.left
            self.right = rect.right
            self.top = rect.top
            self.bottom = rect.bottom
        elif len(args) == 4:
            self.left = args[0]
            self.top = args[1]
            self.right = args[2]
            self.bottom = args[3]
        else:
            self.left = self.right = self.top = self.bottom = 0
        self.x = self.left
        self.y = self.top
        self.width = lambda: self.right - self.left
        self.height = lambda: self.bottom - self.top
        self.centerX = lambda: self.x + self.width()//2
        self.centerY = lambda: self.y + self.height()//2
        self.exactCenterX = lambda: self.x + self.width()/2
        self.exactCenterY = lambda: self.y + self.height()/2

    def isEmpty(self):
        return self.left >= self.right or self.top >= self.bottom

    def setEmpty(self):
        self.__init__()

    def set(self, *args):
        self.__init__(*args)

    def offset(dx, dy):
        self.__init__(self.left, self.top, self.right+dx, self.bottom+dy)

    def offsetTo(dx, dy):
        self.__init__(self.left-dx, self.top-dy, self.right, self.bottom)

    def sort(self):
        if self.isEmpty():
            self.__init__(self.right, self.top, self.left, self.bottom)
            if self.isEmpty():
                self.__init__(self.left, self.bottom, self.right, self.top)
            if self.isEmpty():
                self.__init__(self.right, self.top, self.left, self.bottom)
            if self.isEmpty():
                self.__init__(self.left, self.bottom, self.right, self.top)

    def intersect(self, other):
        if type(other) == Rect:
            return self.intersect((other.left, other.right)) or self.intersect((other.top, other.bottom))
        if type(other) == Point or type(other) == PointF:
            return self.intersect((other.x, other.y))
        elif type(other) == tuple or type(other) == list:
            return (other[0] >= self.left and other[0] <= self.right) and (other[1] >= self.top and other[1] <= self.bottom)

    def contains(self, other):
        if type(other) == Rect:
            return self.contains((other.left, other.right)) or self.contains((other.top, other.bottom))
        if type(other) == Point or type(other) == PointF:
            return self.contains((other.x, other.y))
        elif type(other) == tuple or type(other) == list:
            return (other[0] > self.left and other[0] < self.right) and (other[1] > self.top and other[1] < self.bottom)

    def __str__(self):
        return "<Rect (%s, %s, %s, %s)>" % (self.left, self.top, self.right, self.bottom)


class RectF(Rect):
    def __init__(self, *args):
        super().__init__(*args)
    def round(self, rect=None):
        rect = rect if rect else self
        rect.__init__(round(rect.left), round(rect.top), round(rect.right), round(rect.bottom))
    def roundOut(self, rect=None):
        rect = rect if rect else self
        rect.__init__(math.floor(rect.left), math.floor(rect.top),
            math.floor(rect.right), math.floor(rect.bottom))
