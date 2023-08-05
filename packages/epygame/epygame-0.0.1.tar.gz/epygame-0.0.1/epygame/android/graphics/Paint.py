from ...utils import *
from .Color import Color
from .Typeface import Typeface

class Paint:
    class Align:
        LEFT = 0
        CENTER = 1
        RIGHT = 2
    class Cap:
        BUT = 0
        ROUND = 1
        SQUARE = 2
    class Style:
        FILL = 0
        FILL_AND_STROKE = 1
        STROKE = 2

    def __init__(self, arg=None):
        self.textsize = 20
        self.font = Typeface.create("arial", Typeface.NORMAL)
        self.style = Paint.Style.FILL
        self.aa = False
        self.width = 1
        self.underlined = 0
        self.tf = None
        self.color = (255, 255, 255, 255)
        if type(arg) == Paint:
            self.color = arg.color
            self.textsize = arg.textsize
            self.font = arg.font
            self.style = arg.style
            self.aa = arg.aa
        elif arg:
            self.color = Color.parseColor(arg)

    def set(self, paint): self.__init__(paint)
    def setColor(self, color): self.color = Color.parseColor(color)
    def getColor(self): return self.color
    def setAntiAlias(self, aa): self.aa = aa
    def isAntiAlias(self, aa): return self.aa
    def setStyle(self, style): self.style = style
    def setStrokeWidth(self, w): self.width = w
    def getStrokeWidth(self, w): return self.width
    def setTextSize(self, size):
        self.textsize = size
        self.font.setSize(size)
    def setTypeface(self, tf): self.font = tf
    def getTypeface(self, tf): return self.font
    def setUnderlineText(self, under): self.font.font.set_underline(under)
    def isUnderlineText(self): return self.font.font.get_underline()
    def measureText(self, text): return self.font.size(text)
