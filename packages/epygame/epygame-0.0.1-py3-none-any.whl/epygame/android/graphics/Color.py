class Color:
    BLACK = (0, 0, 0, 225)
    WHITE = (255, 255, 255, 225)
    RED = (255, 0, 0, 225)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    CYAN = (0, 255, 255, 225)
    MAGENTA = (255, 0, 255, 255)
    YELLOW = (255, 255, 0, 255)
    DKGRAY = (68, 68, 68, 255)
    GRAY = (136, 136, 136, 255)
    LTGRAY = (204, 204, 204, 255)
    TRANSPARENT = (0, 0, 0, 0)

    def parseColor(color):
        if type(color) == str:
            color = color.lstrip("#")
            while len(color) < 6:
                color += "f"
            if len(color) == 6:
                color = "FF%s" % color
            while len(color) < 8:
                color += "f"
            clr = (int(color[i:i+2], 16) for i in (2, 4, 6, 0))
            return tuple(clr)
        elif type(color) == int:
            clr = "%s" % hex(color)
            return Color.parseColor(clr[2:])
        elif type(color) == tuple or type(color) == list:
            return tuple(round(i*255) if type(i) == float else i for i in color)
        elif type(color) == dict:
            return (color["r"], color["g"], color["b"], color["a"])
        else:
            return color

    def alpha(color):
        return Color.parseColor(color)[3]
    def red(color):
        return Color.parseColor(color)[0]
    def green(color):
        return Color.parseColor(color)[1]
    def blue(color):
        return Color.parseColor(color)[2]

    def RGBAToHEX(r, g, b, a):
        return hex((a & 0xff) << 24 | (r & 0xff) << 16 | (g & 0xff) << 8 | (b & 0xff))
