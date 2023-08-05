from ...utils import *
from .Bitmap import Bitmap
from .Paint import Paint
from .Rect import Rect, RectF
from .Point import Point, PointF
from .Color import Color

class Canvas:
    def __init__(self, bitmap=None):
        if bitmap:
            self.surface = bitmap.surface
        else:
            self.surface = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.saves = []

    def setBitmap(self, bitmap): self.__init__(bitmap)
    def getHeight(self): return self.surface.get_height()
    def getWidth(self): return self.surface.get_width()
    def drawARGB(self, a, r, g, b): self.surface.fill((r, g, b, a))
    def drawColor(self, color): self.surface.fill(Color.parseColor(color))
    def drawArc(self, *args):
        if len(args) == 8:
            left, top, right, bottom, startAngle, sweepAngle, useCenter, paint = args
        elif len(args) == 5:
            rect, startAngle, sweepAngle, useCenter, paint = args
            left = rect.left
            top = rect.top
            right = rect.right
            bottom = rect.bottom
        pygame.draw.arc(self.surface, paint.color, pygame.Rect(left, top, right, bottom), startAngle, sweepAngle, paint.width)
    def drawBitmap(self, *args):
        if len(args) == 4:
            if type(args[0]) == Bitmap:
                if (type(args[1]) == Rect or type(args[1]) == RectF):
                    self.surface.blit(args[0].surface, (args[1].left, args[1].top), args[2])
                elif type(args[1]) == int or type(args[1]) == float:
                    self.surface.blit(args[0].surface, (args[1], args[2]))
    def drawCircle(self, cx, cy, radius, paint): pygame.draw.circle(self.surface, paint.color, (cx, cy), radius, paint.width)
    def drawLine(self, startX, startY, stopX, stopY, paint): pygame.draw.line(self.surface, paint.color, (startX, startY), (stopX, stopY), paint.width)
    def drawLines(self, pts, offset=0, count=None, paint=None):
        if count: pygame.draw.lines(self.surface, paint.color, True, pts[offset:count+offset], paint.width)
        else: pygame.draw.lines(self.surface, paint.color, True, pts[offset:], paint.width)
    def drawOval(self, *args):
        if len(args) == 5:
            rect = RectF(args[0], args[1], args[2], args[3])
            paint = args[4]
        else: rect, paint = args
        pygame.draw.ellipse(self.surface, paint.color, pygame.Rect(rect.left, rect.top, rect.right, rect.bottom), paint.width)
    def drawPaint(self, paint): self.surface.fill(paint.color)
    def drawPoint(self, x, y, paint): pygame.gfxdraw.pixel(self.surface, x, y, paint.color)
    def drawPoints(self, *args):
        pts = args[0]
        offset = cout = 0
        if len(args) == 4:
            offset = args[1]
            count = args[2]
            paint = args[3]
        else: paint = args[1]
        if count: pts = pts[offset:count+offset]
        else: pts = pts[offset]
        point = pts[0]
        if type(point) == tuple or type(point) == list:
            for i in pts: self.drawPoints(i[0], i[1], paint)
        elif type(point) == int:
            for i in range(len(pts)):
                self.drawPoints(i, i+1, paint)
                continue
        elif type(point) == Point or type(point) == PointF:
            for i in pts: self.drawPoints(i.x, i.y, paint)
    def drawRect(self, *args):
        if len(args) == 5:
            pygame.draw.rect(self.surface, args[4].color, pygame.Rect(args[0], args[1], args[2], args[3]), paint.width)
        elif len(args) == 2:
            pygame.draw.rect(self.surface, args[1].color, pygame.Rect(args[0].left, args[0].top, args[0].right, args[0].bottom), paint.width)
    def drawText(self, bg=0x00000000, *args):
        start = end = 0
        text = ""
        if len(args) == 6:
            text, start, end, x, y, paint = args
        elif len(args) == 4:
            text, x, y, paint = args
        if len(paint.color) == 3:
            paint.color = (paint.color[0], paint.color[1], paint.color[2], 255)
        self.colorkey = (0, 0, 0, 255) if paint.color != (0, 0, 0, 255) else (255, 255, 255, 255)
        if end:
            rendered = paint.font.font.render(text[start:end], paint.aa, paint.color)
        else:
            rendered = paint.font.font.render(text[start:], paint.aa, paint.color, self.colorkey)
        xT, yT, width, height = rendered.get_rect()
        rendered.set_colorkey(self.colorkey)
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(self.colorkey)
        if bg:
            self.surface.fill(Color.parseColor(bg))
        self.surface.blit(rendered, (x, y))
    def rotate(self, degrees): self.surface = pygame.transform.rotate(self.surface, degrees)
    def scale(self, x, y): self.surface = pygame.transform.scale(self.surface, (x, y))
    def save(self):
        self.saves.append(self.surface.copy())
        return len(self.saves)-1
    def restore(self):
        surface = self.saves[len(self.saves)-1]
        self.surface.blit(surface, (0, 0))
    def restoreToCount(self, count):
        surface = self.saves[count]
        self.surface.blit(surface, (0, 0))
