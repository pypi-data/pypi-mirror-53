from ...utils import *
from ...shadowMaker import *
from ..graphics import *
from ...window.App import App

class View:
    def __init__(self, *args, **kwargs):
        self.alpha = 255
        self.clickable = 1
        self.contextClickable = 1
        self.elevation = 0
        self.fadeScrollsbars = 0
        self.focusable = 1
        self.focused = 0
        canvas = Canvas()
        canvas.drawColor(Color.TRANSPARENT)
        self.foreground = Drawable(width=getValue(kwargs, "width", 256), height=getValue(kwargs, "height", 256))
        self.foreground.draw(canvas)
        self.background = Drawable(width=getValue(kwargs, "width", 256), height=getValue(kwargs, "height", 256))
        self.background.draw(canvas)
        self.id = 0
        self.isScrollContainer = 0
        self.keepScreenOn = 0
        self.layerType = 0
        self.longClickable = 1
        self.paddingTop = 0
        self.paddingLeft = 0
        self.paddingRight = 0
        self.paddingBottom = 0
        self.padding = (self.paddingLeft, self.paddingTop, self.paddingRight, self.paddingBottom)
        self.marginTop = 0
        self.marginLeft = 0
        self.marginRight = 0
        self.marginBottom = 0
        self.margin = (self.marginLeft, self.marginTop, self.marginRight, self.marginBottom)
        self.rotation = 0
        self.rotationX = 0
        self.rotationY = 0
        self.scaleX = 1
        self.scaleY = 1
        self.scrollX = 0
        self.scrollY = 0
        self.scrollbarSize = 0
        self.scrollbarStyle = 0
        self.scrollbarThumbHorizontal = 0
        self.scrollbarThumbVertical = 0
        self.scrollbarTrackHorizontal = 0
        self.scrollbarTrackVertical = 0
        self.tag = ""
        self.textAlignment = 0
        self.textDirection = 0
        self.theme = 0
        self.tooltipText = ""
        self.transformPivotX = 0
        self.transformPivotY = 0
        self.translatedX = 0
        self.translatedY = 0
        self.translatedZ = 0
        self.visibility = 0
        self.z = 0
        self.x = 0
        self.y = 0
        self.objects = []
        self.parent = None
        self.enable = 1
        self.orientation = None

        ######### - listeners - #########
        self.onClick = lambda *args, **kwargs: None
        self.onLongClick = lambda *args, **kwargs: None
        self.onCreateContextMenu = lambda *args, **kwargs: None
        self.onDrag = lambda *args, **kwargs: None
        self.onFocusChange = lambda *args, **kwargs: None
        self.onGenericMotion = lambda *args, **kwargs: None
        self.onHover = lambda *args, **kwargs: None
        self.onKey = lambda *args, **kwargs: None
        self.onLayoutChange = lambda *args, **kwargs: None
        self.onScrollChange = lambda *args, **kwargs: None
        self.onTouch = lambda *args, **kwargs: None

        if len(args) == 1:
            if type(args[0]) == App:
                self.background = Bitmap.createBitmap((), args[0].width, args[0].height)
                self.foreground = Canvas(Bitmap.createBitmap((), args[0].width, args[0].height))
                self.foreground.drawColor(Color.TRANSPARENT)
                self.foreground = Drawable(self.foreground)
                args[0].addView(self)
                self.objects = args[0].objects
                self.parent = args[0]
        self.width = self.background.surface.get_width()
        self.height = self.background.surface.get_height()
        self.surface = self.background.surface

    def bringToFront(self):
        self.objects.remove(self)
        self.objects.append(self)
    def draw(self, surface, *args):
        surface.blit(self.background.surface, (self.x+self.translatedX, self.y+self.translatedY))
        surface.blit(self.foreground.surface, (self.x+self.translatedX, self.y+self.translatedY))
    def setTag(self, tag): self.tag = tag
    def getTag(self, tag): return self.tag
    def getAlpha(self): return self.alpha
    def getBottom(self): return self.background.surface.get_rect().y + self.background.surface.get_rect().height
    def getRight(self): return self.background.surface.get_rect().x + self.background.surface.get_rect().width
    def getHeight(self): return self.background.surface.get_rect().height
    def getId(self): return self.id
    def getLeft(self): return self.background.surface.get_rect().x
    def getTop(self): return self.background.surface.get_rect().y
    def getPaddingLeft(self): return self.paddingLeft
    def getPaddingTop(self): return self.paddingTop
    def getPaddingBottom(self): return self.paddingBottom
    def getPaddingRight(self): return self.paddingRight
    def getRotation(self): return self.rotation
    def getRotationX(self): return self.rotationX
    def getRotationY(self): return self.rotationY
    def getScaleX(self): return self.scaleX
    def getScaleY(self): return self.scaleY
    def getScrollX(self): return self.scrollX
    def getScrollY(self): return self.scrollY
    def getVisibility(self): return self.visibility
    def getWidth(self): return self.surface.get_rect().width
    def getX(self): return self.x
    def getY(self): return self.y
    def isClickable(self): return self.clickable
    def isEnabled(self): return self.enable
    def isFocusable(self): return self.focusable
    def isFocused(self): return self.focused
    def scrollBy(self, dx, dy):
        self.scrollX += dx
        self.scrollY += dy
        self.surface.scroll(self.scrollX, self.scrollY)
    def scrollTo(self, dx, dy):
        self.scrollX = dx
        self.scrollY = dy
        self.surface.scroll(self.scrollX, self.scrollY)
    def getForeground(self): return self.foreground
    def setBackgroundColor(self, color):
        self.backgroundColor = Color.parseColor(color)
        self.background.surface.fill(Color.parseColor(color))
    def setBackground(self, back): self.background = back
    def setClickable(self, clickable): self.clickable = clickable
    def setEnabled(self, enable): self.enable = enable
    def getRootView(self): return self.parent
    def setFocusable(self, focusable): self.focusable = focusable
    def setId(self, ID): self.id = ID
    def setOnClickListener(self, function): self.onClick = function
    def setOnLongClickListener(self, function): self.onLongClick = function
    def setOnCreateContextMenuListener(self, function): self.onCreateContextMenu = function
    def setOnFocusChangeListener(self, function): self.onFocusChange = function
    def setOnTouchListener(self, function): self.onTouch = function
    def setPadding(self, left, top, right, bottom):
        self.paddingTop = top
        self.paddingLeft = left
        self.paddingRight = right
        self.paddingBottom = bottom
        self.padding = (self.paddingLeft, self.paddingTop, self.paddingRight, self.paddingBottom)
    def setMargin(self, left, top, right, bottom):
        self.marginTop = top
        self.marginLeft = left
        self.marginRight = right
        self.marginBottom = bottom
        self.margin = (self.marginLeft, self.marginTop, self.marginRight, self.marginBottom)
    def setVisibility(self, visible): self.visibility = visibility
    def translateX(self, x):
        self.x = x
        self.translatedX = x
    def translateY(self, y):
        self.y = y
        self.translatedY = y
    def translateZ(self, z):
        self.objects.remove(self)
        self.objects.insert(z, self)
    def setSize(self, width, height):
        self.width = width
        self.height = height
        if width == "match_parent":
            self.width = self.parent.width - self.parent.paddingLeft - self.paddingRight
        if height == "match_parent":
            self.height = self.parent.height - self.parent.paddingTop - self.paddingBottom
        background = self.background.surface.copy()
        foreground = self.foreground.surface.copy()
        bitmap = Bitmap.createBitmap((), self.width, self.height)
        self.background = Canvas(bitmap)
        self.foreground = Canvas(bitmap)
        self.background.surface.blit(background, (0, 0), (0, 0, self.width, self.height))
        self.foreground.surface.blit(foreground, (0, 0), (0, 0, self.width, self.height))
        self.surface = self.background.surface
    def getRect(self):
        return RectF(self.x, self.y, self.width+self.x, self.height+self.y)
    def setElevation(self, offset=(0, 0), ambience=0.8, shadow_scale=0.99):
        canvas = Canvas()
        canvas.drawColor(Color.TRANSPARENT)
        canvas.surface = copy(self.background.surface)
        canvas.surface = add_shadow(self.background.surface, offset, shadow_scale=shadow_scale, ambience=ambience)
        background = Drawable(width=canvas.surface.get_width(), height=canvas.surface.get_height())
        background.draw(canvas)
        self.setBackground(background)

    def setMaterialShadowCenter(self, size=1, ambience=0.95, shadow_scale=0.99):
        while size > 0:
            self.setElevation((size-1, size), ambience, shadow_scale)
            self.setElevation((size, size-1), ambience, shadow_scale)
            self.setElevation((size+1, size), ambience, shadow_scale)
            self.setElevation((size, size+1), ambience, shadow_scale)
            self.setElevation(((-size)-1, (-size)), ambience, shadow_scale)
            self.setElevation(((-size), (-size)-1), ambience, shadow_scale)
            self.setElevation(((-size)+1, (-size)), ambience, shadow_scale)
            self.setElevation(((-size), (-size)+1), ambience, shadow_scale)
            size -= 1

    def setMaterialShadowDown(self, size=1, ambience=0.95, shadow_scale=0.99):
        while size > 0:
            self.setElevation((size, size-1), ambience, shadow_scale)
            self.setElevation((size+1, size), ambience, shadow_scale)
            self.setElevation((size-1, size), ambience, shadow_scale)
            size -= 1
        
    def setElevationBlur(self, offset=(0, 0), ambience=0.8, shadow_scale=1.0):
        if offset[0] != 0 and offset[1] != 0:
            a = divmod(offset[0], offset[1])[0] if offset[0] > offset[1] else divmod(offset[1], offset[0])[0]
            for i in range(offset[0] if offset[0] < offset[1] else offset[1]):
                self.setElevation((i, i+a) if offset[0] < offset[1] else (i+a, i), ambience, shadow_scale)
