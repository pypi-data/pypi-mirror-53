from ..view import *

class LinearLayout(ViewGroup):
    def __init__(self, *args, **kwargs):
        super(LinearLayout, self).__init__(*args, **kwargs)
        self.orientation = "vertical"

    def draw(self, surface, orientation="vertical"):
        super(LinearLayout, self).draw(surface, self.orientation)

    def setOrientation(self, orientation): self.orientation = orientation
