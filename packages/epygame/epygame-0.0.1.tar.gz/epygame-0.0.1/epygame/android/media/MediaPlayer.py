from ...utils import *
from ...window.App import App

class MediaPlayer:
    def create(*args):
        return MediaPlayer(*args)

    def __init__(self, *args, **kwargs):
        self.app = None
        self.path = ""
        self.music = None
        self.looping = 0
        self.playing = 0
        self.paused = 0
        if len(args) == 1:
            if type(args[0]) == App: self.app = args[0]
            elif type(args[0]) == str: self.path = args[0]
        elif len(args) == 2:
            if type(args[0]) == App:
                self.app, self.path = args
            elif type(args[0]) == str:
                self.path, self.app = args
        if self.path:
            self.music = pygame.mixer.music
            self.music.load(self.path)
    def setVolume(self, volume):
        if self.music: self.music.set_volume(volume)
    def getVolume(self):
        if self.music: return self.music.get_volume()
    def getCurrentPosition(self):
        if self.music: return self.music.get_pos()
    def getDuration(self):
        if self.path: return pygame.mixer.Sound(self.path).get_length()
    def isLooping(self): return self.looping
    def isPlaying(self): return self.playing
    def pause(self):
        if self.music:
            self.playing = 0
            self.paused = 1
            self.music.pause()
    def release(self):
        if self.music:
            self.playing = 0
            self.looping = 0
            self.music.unload()
    def seekTo(self, pos):
        if self.music:
            self.music.set_pos(pos)
    def setDataSource(self, source):
        self.path = source
        if self.path:
            self.music = pygame.mixer.music
            self.music.load(self.path)
    def setLooping(self, loop):
        if loop:
            self.looping = 1
        else:
            self.looping = 0
    def setNextMediaPlayer(self, mp):
        if type(mp) == MediaPlayer:
            if self.music:
                self.music.queue(mp.path)
    def start(self):
        if self.paused:
            self.paused = 0
            if self.music:
                self.music.unpause()
        else:
            if self.music:
                self.music.play(-1 if self.looping else 1)
    def stop(self):
        if self.music:
            self.music.stop()
            self.playing = 0
            self.paused = 0
