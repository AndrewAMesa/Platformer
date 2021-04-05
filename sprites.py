import pygame, sys
pygame.init()
#class MainCharacter:


#class Platform:

class Collectables(pygame.sprite.Sprite):
    def __init__(self, string, xpos, ypos, image):
        super().__init__()
        self.name = string
        self.xpos = xpos
        self.ypos = ypos
        self.rect.update(xpos, ypos, 100, 100)
        self.image=pygame.image.load(image)

    def is_collided_with(self, char):

        if self.rect.colliderect(char.rect):

            self.kill()

    def getname(self):
        return self.name

    def updatepos(self, x, y):
        self.posx = x
        self.posy = y

    def getposx(self):
        return self.posx

    def getposy(self):
        return self.posy