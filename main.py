import sys
import pygame
from pygame.locals import *
from sprites import *

pygame.init()
fpsClock = pygame.time.Clock()

##############
#Image
##############
sword_image = pygame.image.load("Images/Sword.png")

TILESIZE = 30
FPS = 60
GRAVITY = 1

if infoObject.current_h == 720:
    GRAVITY = GRAVITY * 0.667
infoObject = pygame.display.Info()
DISPLAYSURF = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

#platform1 = Platform(pygame.image.load('Images/TestPlatform.png'), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, False, 0)
#platform2 = Platform(pygame.image.load('Images/TestPlatform.png'), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, False, 0)
platform_group = pygame.sprite.Group()
#platform_group.add(platform1)
#platform_group.add(platform2)


sword = Sword(DISPLAYSURF.get_width()/2+21, DISPLAYSURF.get_height()/2+14, sword_image)
current_weapon = pygame.sprite.Group()
current_weapon.add(sword)

main_character = MainCharacter(DISPLAYSURF)
character_group = pygame.sprite.Group()
character_group.add(main_character)

enemy = BasicEnemy(DISPLAYSURF, DISPLAYSURF.get_width() + 50, int(DISPLAYSURF.get_height()/2), 30, 30)

clockObj = pygame.font.Font('freesansbold.ttf', 20)
timeLeft = 500

def display_time(milliseconds):
    clockSurfaceObj = clockObj.render("TimeLeft: " + str(timeLeft - int(milliseconds/60)), True, (255, 255, 255))
    DISPLAYSURF.blit(clockSurfaceObj, (DISPLAYSURF.get_width() - 143, 10))
def update_all():
    sword.update()
    character_group.update(sword)
    shiftX, shiftY = main_character.getShift()
    platform_group.update(shiftX, shiftY)

    #for collectable in collectable_group:
    #    collectable.is_collided_with(main_character)
    check_y_collisions()


def check_y_collisions():
    if checkStanding(main_character) and main_character.y_velocity != main_character.jump_height:
        main_character.y_velocity = 0
    elif main_character.y_velocity + GRAVITY < 0:
        main_character.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.top + main_character.y_velocity < platform.rect.bottom < main_character.rect.top and not platform.walkthrough:
                    main_character.y_velocity = 0

    else:
        main_character.y_velocity += GRAVITY
        sword.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.bottom + main_character.y_velocity > platform.rect.top > main_character.rect.bottom and not platform.walkthrough:
                    main_character.y_velocity = 0



def check_x_collisions():
    if main_character.x_velocity != 0:
        for platform in platform_group:
            if main_character.rect.bottom > platform.rect.top and main_character.rect.top < platform.rect.bottom:
                if main_character.x_velocity > 0:
                    if main_character.rect.right + main_character.x_velocity >= platform.rect.left >= main_character.rect.right and not platform.walkthrough:
                        return "Right"
                if main_character.x_velocity < 0:
                    if main_character.rect.left + main_character.x_velocity <= platform.rect.right <= main_character.rect.left and not platform.walkthrough:
                        return "Left"
    return "None"


def checkStanding(character):
    for platform in platform_group:
        if character.rect.bottom == platform.rect.top:
            if character.rect.left < platform.rect.right and character.rect.right > platform.rect.left and not platform.walkthrough:
                return True


def main():
    milliseconds = 0
    readFile(0)
    while True:
        DISPLAYSURF.fill((0, 0, 0))
        update_all()
        current_weapon.draw(DISPLAYSURF)
        character_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)

        main_character.displayhealth(DISPLAYSURF)
        display_time(milliseconds)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            main_character.direction = 1
            main_character.x_velocity = 5
            if check_x_collisions() == "Right":
                main_character.x_velocity = 0
        elif keys[pygame.K_a]:
            main_character.direction = -1
            main_character.x_velocity = -5
            if check_x_collisions() == "Left":
                main_character.x_velocity = 0
        else:
            main_character.x_velocity = 0
        # Event Loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if checkStanding(main_character):
                        main_character.jump(sword)
                if event.key == K_RETURN:
                        sword.attacking = True





        # Update the Screen
        pygame.display.update()
        fpsClock.tick(FPS)
        milliseconds += fpsClock.tick_busy_loop(560)
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
                
    shiftSize = 120
    if infoObject.current_h == 720:
        shiftSize = 80

    for i in range(lenX):
        for j in range(lenY):
            if b[i][j] == "L":
                platform_group.add(LavaBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize), (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "J":
                platform_group.add(DoubleUpgrade((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize), (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "A":
                platform_group.add(AddHealth((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize), (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "S":
                platform_group.add(SpikesBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize), (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))



main()
