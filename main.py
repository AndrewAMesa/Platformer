import pygame, sys
from pygame.locals import *
from sprites import *
pygame.init()


class Main:
    DISPLAYWIDTH = 15
    DISPLAYHEIGHT = 15
    TILESIZE = 30
    DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH * TILESIZE, DISPLAYHEIGHT * TILESIZE))

    #Images
    swordImage = pygame.image.load("Images/Sword.png")

    #Sprites
    sword = Sword(40, 40, swordImage)

    #Sprite Groups
    currentWeapon = pygame.sprite.Group()
    currentWeapon.add(sword)

    def main(self):

        while True:
            self.currentWeapon.draw(self.DISPLAYSURF)
            # Event Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Update the Screen
            pygame.display.update()


MainObject = Main()
MainObject.main()
