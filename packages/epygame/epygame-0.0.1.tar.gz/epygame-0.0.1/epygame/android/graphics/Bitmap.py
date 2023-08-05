from ...utils import *
from .Color import Color

class Bitmap:
    class Config:
        ALPHA_8 = 0
        ARGB_4444 = 1
        ARGB_8888 = 2
        RGBA_F16 = 3
        RGB_565 = 4

    def createBitmap(*args):
        return Bitmap(*args)

    def createScaledBitmap(bitmap, dstWidth, dstHeight):
        colors = []
        newW = int(dstWidth)
        newH = int(dstHeight)
        newSurface = pygame.transform.scale(bitmap.surface, (newW, newH))
        for x in range(newW):
            for y in range(newH):
                colors.append(newSurface.get_at((x, y)))
        return Bitmap(colors, newW, newH)

    def __init__(self, *args):
        if len(args) == 3:
            if type(args[0]) == tuple or type(args[0]) == list:
                self.width = args[1]
                self.height = args[2]
                self.preclrs = args[0]
                self.colors = splitList(tuple(Color.parseColor(i) for i in args[0]), self.height)
        elif len(args) == 1:
            if type(args[0]) == Bitmap:
                bitmap = args[0]
                self.width = bitmap.width
                self.height = bitmap.height
                self.preclrs = bitmap.preclrs
                self.colors = splitList(tuple(Color.parseColor(i) for i in bitmap.preclrs), self.height)
        elif len(args) == 5:
            if type(args[0]) == Bitmap:
                bitmap = args[0]
                x, y = args[1], args[2]
                self.width = args[3]
                self.height = args[4]
                self.preclrs = bitmap.preclrs
                cx = 0
                for i in range(x):
                    cy = 0
                    for j in range(y):
                        bitmap.colors[i+cx][j+cy] = (0, 0, 0)
                        cy += 1
                    cx += 1
                self.colors = splitList(tuple(Color.parseColor(i) for i in bitmap.preclrs), self.height)
        self.surface = pygame.Surface((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                if len(self.colors)-1 >= x and len(self.colors[x])-1 >= y:
                    pygame.gfxdraw.pixel(self.surface, x, y, self.colors[x][y])

    def getColor(self, x, y):
        return self.colors[x][y]

    def copy(self):
        return Bitmap(self.preclrs, self.width, self.height)

    def getPixel(self, x, y):
        return Color.RGBAToHEX(self.colors[x][y])

    def eraseColor(self, color=(255, 255, 255, 255)):
        self.surface.fill(color)

    def getWidth(self): return self.width
    def getHeight(self): return self.height
    def setWidth(self, width): self.__init__(self.colors, width, self.height)
    def setHeight(self, width): self.__init__(self.colors, self.width, height)
    def setPixel(self, x, y, color):
        self.colors[x][y] = Color.parseColor(color)
        pygame.gfxdraw.pixel(self.surface, x, y, self.colors[x][y])

    def getPixels(self, pixels=[], offset=0, stride=0, x=0, y=0, width=0, height=0):
        returnPixels = []
        for x in pixels:
            for y in pixels[x]:
                returnPixels.append(self.getPixel(x, y))
        return returnPixels[offset:]
