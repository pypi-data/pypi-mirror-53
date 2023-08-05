from ..utils import *
from ..android.graphics.Rect import Rect, RectF
from ..android.graphics.Point import Point, PointF

class App:
    def __init__(self, *args, **kwargs):
        self.windowName = getValue(kwargs, "name", "Window")
        self.icon = getValue(kwargs, "icon")
        self.width = getValue(kwargs, "width", 720)
        self.height = getValue(kwargs, "height", 480)
        self.fps = getValue(kwargs, "fps", 60)
        self.onUpdate = lambda *args: None
        self.current_activity = getValue(kwargs, "mainActivity", "Main")
        self.focusedView = None
        self.currentXPrint = 0
        self.debugSize = 14
        self.activities = {
            "Main" : {
                "class" : None,
                "objects" : []
                }
            }
        if self.icon: self.setAppIcon(self.icon)
        self.setAppName(self.windowName)
        self.setAppIcon(self.icon)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.debugs = []
        self.goActivity(self.current_activity)

    def setFramerateLimit(self, fps): self.fps = fps
    def getCurrentFramerate(self): return self.clock.get_fps()
    def printDebug(self, text, color=0xFFFFAACC, size=14):
        self.debugSize = size
        textview = TextView()
        textview.translateY(self.currentXPrint)
        textview.setText(text)
        textview.setTextSize(self.debugSize)
        textview.setTextColor(color)
        textview.setElevation((1, 1))
        self.addDebug(textview)
        self.currentXPrint += round(self.debugSize)

    def clearDebug(self): self.debugs = []

    def activity(self, clss):
        self.activities[clss.__name__] = {"class" : clss, "objects" : []}
        self.objects = self.activities[clss.__name__]["objects"]
        self.activities[clss.__name__]["class"] = self.activities[clss.__name__]["class"]()

    def goActivity(self, name):
        self.objects = self.activities[name]["objects"]
        self.objects = []
        if self.activities[name]["class"]:
            newWindow = self.activities[name]["class"].initialize(self)
            if newWindow:
                self = newWindow

    def start(self):
        self.goActivity(self.current_activity)
        while True:
            self.onUpdate(self)
            self.draw()
            self.handle_events()
            pygame.display.update()
            self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill((255, 255, 255, 255))
        for objId in self.objects:
            objId.draw(self.screen)
        for obj in self.debugs:
            obj.draw(self.screen)

    def addView(self, view):
        if not view.id:
            view.id = len(self.objects)
        self.objects.append(view)
        view.z = len(self.objects)-1
        view.objects = self.objects
        return self.objects[view.id]

    def addDebug(self, view):
        self.debugs.append(view)
        view.objects = self.debugs
        return self.debugs[view.id]

    def removeView(self, view): self.objects.remove(view)

    def findViewById(self, vid):
        if vid in self.objects:
            return self.objects[vid]
        else: return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pos = PointF(pos[0], pos[1])
                    for view in self.objects:
                        try:
                            for view1 in view.getViews():
                                rect = view1.getRect()
                                if rect.intersect(pos): view1.onClick(pos)
                        except:
                            rect = view.getRect()
                            if rect.intersect(pos): view.onClick(pos)
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN and pressed[0]:
                pos = pygame.mouse.get_pos()
                pos = PointF(pos[0], pos[1])
                for view in self.objects:
                    try:
                        for view1 in view.getViews():
                            rect = view1.getRect()
                            if rect.intersect(pos): view1.onTouch(pos, pressed[0])
                    except:
                        rect = view.getRect()
                        if rect.intersect(pos): view.onTouch(pos, pressed[0])

    def setOnUpdate(self, function):
        self.onUpdate = function

    def setAppName(self, name):
        pygame.display.set_caption("%s" % name)

    def setAppIcon(self, path):
        if path:
            pygame.display.set_icon(pygame.image.load(path))
from ..android.widget.TextView import TextView
