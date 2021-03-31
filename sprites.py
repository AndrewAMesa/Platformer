import pygame, sys
from pygame.locals import *

class MainCharacter:
    print("hi")
class Platform:
    print("hi")

class Sword:
    def __init__(self, _left, _top, _image):
        pygame.sprite.Sprite.__init__(self)
        self.left = _left
        self.top = _top
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.rect.width, self.rect.height)
        self.count = 0
        self.xMove = 0
        self.yMove =0