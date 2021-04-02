import sys
import pygame
from pygame.locals import *
from LevelInterpreter import *
from sprites import *

pygame.init()

DISPLAYWIDTH = 15
DISPLAYHEIGHT = 15
TILESIZE = 30
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH * TILESIZE, DISPLAYHEIGHT * TILESIZE))

main_character = MainCharacter(DISPLAYSURF)
character_group = pygame.sprite.Group()
character_group.add(main_character)

platform1 = Platform(DISPLAYSURF)
platform_group = pygame.sprite.Group()
platform_group.add(platform1)


def main():

    while True:
        character_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)

        # Event Loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update the Screen
        pygame.display.update()


main()
