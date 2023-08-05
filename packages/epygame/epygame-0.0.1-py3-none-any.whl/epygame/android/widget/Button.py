from ...utils import *
from ..graphics import *
from ..view import *
from .TextView import TextView

class Button(TextView):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__( *args, width=125, height=50)
        self.backgroundColor = Color.LTGRAY
        self.setBackgroundColor(self.backgroundColor)

    def setText(self, text):
        super(Button, self).setText(text)
        print(self.width1, self.height1, self.h, self.w)
        self.setPadding(self.currentBound.x//4, self.currentBound.y//4, self.currentBound.x//4, self.currentBound.y//4)
        super(Button, self).setText(text)
