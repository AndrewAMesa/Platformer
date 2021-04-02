import pygame, sys
from pygame.sprite import *

class MainCharacter:
    print("hi")
class Platform:
    print("hi")

class Sword (pygame.sprite.Sprite):
    def __init__(self, _left, _top, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(_left, _top, self.rect.width, self.rect.height)
        self.xMove = 0
        self.yMove = 0