from ..view import *

class FrameLayout(ViewGroup):
    def __init__(self, *args, **kwargs):
        super(FrameLayout, self).__init__(*args, **kwargs)

    def draw(self, surface, orientation="vertical"):
        super(FrameLayout, self).draw(surface, "")
