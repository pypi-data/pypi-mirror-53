from ...utils import *
from ..graphics import *
from ..view import *

class TextView(View):
    def __init__(self, *args, **kwargs):
        super(TextView, self).__init__(*args, **kwargs)
        self.text = ""
        self.textSettings = Paint(0xFF212121)
        self.textSettings.setTextSize(24)
        self.backgroundColor = Color.TRANSPARENT
        self.textLinkSettings = Paint(self.textSettings)
        self.textLinkSettings.setColor(Color.parseColor(0xFFAA8899))
        self.linkFind = 0
        self.w = self.h = 0
        self.ttxt = {}
        self.offset = (0, 0)
        self.ambience = 0
        self.shadow_scale = 0

    def setText(self, text):
        canvas = Canvas()
        canvas.drawColor(self.backgroundColor)
        background = Drawable(width=self.width, height=self.height)
        background.draw(canvas)
        self.setBackground(background)
        self.currentBound = RectF(self.paddingLeft, self.paddingTop, self.width, self.height)
        self.background.setBounds(self.currentBound)
        self.text = text
        try:
            self.txt = {i : {"symbol" : text[i],
                        "paint" : getValue(self.ttxt[i], "paint", self.textSettings),
                        "bg" : getValue(self.ttxt[i], "bg", self.backgroundColor)}
                    for i in range(len(text))}
        except Exception as e:
            self.txt = {i : {"symbol" : text[i],
                        "paint" : self.textSettings,
                        "bg" : self.backgroundColor}
                    for i in range(len(text))}
            self.ttxt = {i : self.txt[i] for i in self.txt}
        if self.linkFind:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),#]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            for url in urls:
                a = text.find(url)
                b = a+len(url)-1
                for s in self.txt:
                    if s >= a and s <= b:
                        self.txt[s]["paint"] = self.textLinkSettings
        self.width1 = self.height1 = 0
        for s in self.txt:
            if self.currentBound.x >= self.width - self.w+1+self.padding[2]:
                self.currentBound.x = self.paddingLeft
                self.currentBound.y += self.h
            elif self.currentBound.y >= self.height - self.h+1+self.padding[3]: break
            else:
                self.height1 += self.h
                self.width1 += self.currentBound.x
            self.drawSymbol(self.txt[s]["symbol"], self.txt[s]["bg"], self.txt[s]["paint"])
            self.currentBound.x += self.w

    def drawSymbol(self, s, backgroundColor=None, paint=None):
        canvas = Canvas()
        canvas.drawColor(Color.TRANSPARENT)
        canvas.drawText(backgroundColor, s, 0, 0, paint)
        self.h = canvas.surface.get_height()
        self.w = canvas.surface.get_width()
        self.background.draw(canvas)
        self.background.setBounds(self.currentBound)

    def getText(self):
        return self.text

    def setTextSize(self, textsize):
        self.textSettings.setTextSize(textsize)
        self.setText(self.text)

    def setTextColor(self, color):
        self.textSettings.setColor(color)
        self.setText(self.text)

    def setLinkColor(self, color):
        self.textLinkSettings.setColor(color)
        self.setText(self.text)

    def setAutoFindLinks(self, linkFind):
        self.linkFind = linkFind

    def getChar(self, s):
        return self.txt[s]["symbol"]

    def setChar(self, num, s):
        self.text[num] = s

    def setCharColor(self, num, color):
        self.ttxt[num]["paint"] = Paint(self.ttxt[num]["paint"])
        self.ttxt[num]["paint"].setColor(color)
        self.setText(self.text)

    def setCharsColor(self, num1, num2, color):
        for i in range(num1, num2):
            self.setCharColor(i, color)

    def getCharColor(self, num):
        return self.ttxt[num]["paint"].color

    def setCharBgColor(self, num, color):
        self.ttxt[num]["bg"] = color
        self.setText(self.text)

    def setCharsBgColor(self, num1, num2, color):
        for i in range(num1, num2):
            self.setCharBgColor(i, color)

    def length(self):
        return len(self.text)
