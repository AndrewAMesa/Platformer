import sys
import pygame
from pygame.locals import *
from LevelInterpreter import *
from sprites import *

pygame.init()
fpsClock = pygame.time.Clock()

DISPLAYWIDTH = 15
DISPLAYHEIGHT = 15
TILESIZE = 30
FPS = 60
GRAVITY = 1
infoObject = pygame.display.Info()
DISPLAYSURF = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

platform1 = Platform(pygame.image.load('Images/TestPlatform.png'), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, False, 0)
platform2 = Platform(pygame.image.load('Images/TestPlatform.png'), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, False, 0)
platform_group = pygame.sprite.Group()
platform_group.add(platform1)
platform_group.add(platform2)

main_character = MainCharacter(DISPLAYSURF)
character_group = pygame.sprite.Group()
character_group.add(main_character)


def update_all():
    if checkStanding(main_character) and main_character.y_velocity != main_character.jump_height:
        main_character.y_velocity = 0
    elif main_character.y_velocity + GRAVITY < 0:
        main_character.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.top + main_character.y_velocity < platform.rect.bottom < main_character.rect.top:
                    main_character.rect.top = platform.rect.bottom
                    main_character.y_velocity = 0
    else:
        main_character.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.bottom + main_character.y_velocity > platform.rect.top > main_character.rect.bottom:
                    main_character.rect.bottom = platform.rect.top
                    main_character.y_velocity = 0
    character_group.update()
    shiftX, shiftY = main_character.getShift()
    for platform in platform_group:
        platform.update(shiftX, shiftY)

def checkStanding(character):
    for platform in platform_group:
        if character.rect.bottom == platform.rect.top:
            if character.rect.left < platform.rect.right and character.rect.right > platform.rect.left:
                return True


def main():
    readFile(0)
    while True:
        DISPLAYSURF.fill((0, 0, 0))
        update_all()
        character_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)

        # Event Loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_w:
                    if checkStanding(main_character):
                        main_character.jump()

        # Update the Screen
        pygame.display.update()

        fpsClock.tick(FPS)


def readFile(levelNum):
    timeStr = ""
    lvlTime = -1

    a = []

    f = open("Levels/Level" + str(levelNum), "r")

    for x in f:
        if "t" not in x:
            c = []
            for i in x:
                if i != "\n":
                    c.append(i)

            a.append(c)

        elif "t" in x:
            timeStr = x
            timeStr = timeStr.replace("t", "")
            lvlTime = int(timeStr)

    lenX = len(a)
    lenY = len(a[0])

    b = []

    for i in range(lenY):
        d = []
        for j in range(lenX):
            d.append(0)

        b.append(d)

    lenX = len(b)
    lenY = len(b[0])

    # inverting the map
    for i in range(lenX):
        for j in range(lenY):
            b[i][j] = a[j][i]

    startingPosX = 0
    startingPosY = 0

    for i in range(lenX):
        for j in range(lenY):
            if b[i][j] == "P":
                startingPosX = i
                startingPosY = j
                exit

    for i in range(lenX):
        for j in range(lenY):
            if b[i][j] == "L":
                platform_group.add(LavaBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * 120), (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * 120)))


main()