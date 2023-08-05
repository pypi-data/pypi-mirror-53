import pygame
import pygame.gfxdraw
from threading import Thread
from copy import copy, deepcopy
import time
import sys
import os
import re

pygame.init()
pygame.font.init()
pygame.mixer.init()

def getValue(kwargs, string, e=None):
    return kwargs[string] if string in kwargs else e

def splitList(lst, number):
    number -= 1
    splitted = [[]]
    current = 0
    count = 0
    for i in lst:
        if count < number:
            splitted[current].append(i)
            count += 1
        else:
            splitted[current].append(i)
            count = 0
            current += 1
            splitted.append([])
    if not splitted[len(splitted)-1]:
        splitted.pop()
    return splitted


class ThStart(Thread):
    def __init__(self, function, *args, **kwargs):
        Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def run(self):
        self.function(*self.args, **self.kwargs)
