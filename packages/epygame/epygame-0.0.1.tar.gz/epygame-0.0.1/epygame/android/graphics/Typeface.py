from ...utils import *
from .Color import Color

class Typeface:
    NORMAL = 0
    BOLD = 1
    ITALIC = 2
    BOLD_ITALIC = 3

    def create(*args): return Typeface(*args)
    def createFromFile(file): return Typeface(file)

    def __init__(self, *args, **kwargs):
        self.textsize = kwargs["textsize"] if "textsize" in kwargs else 20
        self.font = pygame.font.SysFont(getValue(kwargs, "name", "arial"), self.textsize)
        self.style = Typeface.NORMAL
        self.italic = 0
        self.bold = 0
        if len(args) == 2:
            if type(args[0]) == str:
                self.font = pygame.font.SysFont(args[0], self.textsize)
                self.style = args[1]
            elif type(args[0]) == Typeface:
                self.font = args[0].font
                self.style = args[1]
        elif len(args) == 1:
            if type(args[0]) == str:
                self.font = pygame.font.Font(args[0], self.textsize)
        elif len(args) == 3:
            self.font = args[0].font
            self.style = args[0].style
            self.italic = args[2]

        if self.style == Typeface.BOLD:
            self.bold = 1
        elif self.style == Typeface.ITALIC:
            self.italic = 1
        elif self.style == Typeface.BOLD_ITALIC:
            self.bold = 1
            self.italic = 1
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)

    def getStyle(self): return self.style
    def isBold(self): return self.bold
    def isItalic(self): return self.italic
    def setSize(self, size):
        self.textsize = size
        self.__init__(self, self.style, textsize=self.textsize)
