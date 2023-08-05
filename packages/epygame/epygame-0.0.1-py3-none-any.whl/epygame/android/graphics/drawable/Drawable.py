from ....utils import *
from ..Canvas import Canvas
from ..Bitmap import Bitmap
from ..Rect import Rect, RectF
from ..Paint import Paint
from ..Point import Point, PointF

class Drawable:
    def createFromPath(path): return Drawable(path)
    def __init__(self, *args, **kwargs):
        self.surface = pygame.Surface((getValue(kwargs, "width", 256), getValue(kwargs, "height", 256)), pygame.SRCALPHA)
        self.visibility = 1
        self.bounds = Rect(0, 0, getValue(kwargs, "width", 256), getValue(kwargs, "height", 256))
        self.boundsChanged = lambda *args: None
        self.levelChanged = lambda *args: None
        self.level = 0
        if len(args) == 1:
            if type(args[0]) == str:
                self.surface = pygame.image.load(args[0])
    def setVisible(self, visible, restart): self.visibility = visible
    def isVisible(self): return self.visibility
    def setAlpha(self, alpha): self.surface.set_alpha(alpha)
    def draw(self, canvas):
        if type(canvas) == Canvas:
            self.surface.blit(canvas.surface, (self.bounds.x, self.bounds.y), (0, 0, self.bounds.width(), self.bounds.height()))
        else: raise TypeError("first argument must be Canvas, getted %s" % type(canvas))
    def setBounds(self, *args):
        if len(args) == 4:
            self.bounds = Rect(args[0], args[1], args[2], args[3])
            self.boundsChanged(self.bounds)
        elif len(args) == 1:
            self.bounds = args[0]
            self.boundsChanged(self.bounds)
    def getBounds(self): return self.bounds
    def copyBounds(self): return deepcopy(self.bounds)
    def setLevel(self, level):
        self.level = level
        self.levelChange(level)
    def getLevel(self): return self.level
    def getInstrictWidth(self): return self.surface.get_width()
    def getInstrictWidtHeight(self): return self.surface.get_height()
    def onBoundsChange(self, *args, **kwargs): 
        def a(function): ThStart(function, *args, **kwargs)
        return a
    def onLevelChange(self, *args, **kwargs): 
        def a(function): ThStart(function, *args, **kwargs)
        return a
