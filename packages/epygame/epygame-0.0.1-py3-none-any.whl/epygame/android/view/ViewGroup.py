from .View import *

class ViewGroup(View):
    def __init__(self, *args, **kwargs):
        View.__init__(self, *args, **kwargs)
        self.views = []

    def addView(self, view):
        self.views.append(view)
        view.objects = self.views
        view.parent = self
        return self.views[len(self.views)-1]

    def removeView(self, view):
        self.views.remove(view)
        view.objects = []
        view.parent = None

    def getViews(self, views=None):
        for view in self.views if not views else views:
            try:
                a = view.getViews()
                for v in self.getViews(a):
                    yield v
            except:
                yield view

    def draw(self, surface, orientation="vertical"):
        currentX = self.x + self.paddingLeft
        currentY = self.y + self.paddingTop
        self.background.surface.fill(self.backgroundColor)
        for view in self.views:
            view.x = currentX + view.marginLeft
            view.y = currentY + view.marginTop
            w = self.width - self.paddingRight - currentX - view.marginRight - self.paddingLeft*2
            h = self.height - self.paddingBottom - currentY - view.marginBottom - self.paddingTop*2

            if h - view.height <= view.marginTop: h -= view.marginTop
            if w - view.width <= view.marginLeft: w -= view.marginLeft

            if view.width >= w and view.height >= h: view.setSize(w, h)
            elif view.width >= w: view.setSize(w, view.height)
            elif view.height >= h: view.setSize(view.width, h)

            view.draw(self.background.surface, view.orientation)

            if orientation == "vertical": currentY += view.getHeight() + view.marginBottom
            elif orientation == "horizontal": currentX += view.getWidth() + view.marginRight

        surface.blit(self.background.surface, (self.x, self.y))
        surface.blit(self.foreground.surface, (self.x, self.y))

    def bringChildToFront(self, view):
        if view in self.views:
            self.views.remove(view)
            self.views.append(view)
