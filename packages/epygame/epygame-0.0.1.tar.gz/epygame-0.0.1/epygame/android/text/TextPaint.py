from ...utils import *
from ..graphics.Paint import *

class TextPaint(Paint):
    def __init__(self, tp=None):
        self.bgColor = Color.BLACK
        self.underlineColor = Color.WHITE
        self.paint = Paint(Color.WHITE)
        self.linkColor = Color.RED
        if len(args) == 1:
            if type(args[0]) == TextPaint:
                self.bgColor = args[0].bgColor
                self.underlineColor = args[0].underlineColor
                self.paint = args[0].paint
                self.linkColor = args[0].linkColor
            elif type(args[0]) == Paint:
                self.paint = args[0]
    def set(self, tp):
        self.__init__(tp)
