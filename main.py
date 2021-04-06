import sys
import pygame
from pygame.locals import *
from LevelInterpreter import *
from sprites import *

pygame.init()
fpsClock = pygame.time.Clock()

##############
#Image
##############
sword_image = pygame.image.load("Images/Sword.png")

DISPLAYWIDTH = 15
DISPLAYHEIGHT = 15
TILESIZE = 30
FPS = 60
GRAVITY = 1
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH * TILESIZE, DISPLAYHEIGHT * TILESIZE))
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

platform1 = Platform(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, False, 0, pygame.image.load('Images/TestPlatform.png'))
platform2 = Platform(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, False, 0, pygame.image.load('Images/TestPlatform.png'))
platform_group = pygame.sprite.Group()
platform_group.add(platform1)
platform_group.add(platform2)

main_character = MainCharacter(DISPLAYSURF)
character_group = pygame.sprite.Group()
character_group.add(main_character)

sword = Sword(DISPLAYSURF.get_width() / 2 + 5, DISPLAYSURF.get_height() / 2 - 5, sword_image)
current_weapon = pygame.sprite.Group()
current_weapon.add(sword)

def update_all():
    if checkStanding(main_character) and main_character.y_velocity != main_character.jump_height:
        main_character.y_velocity = 0
        sword.y_velocity = 0
    elif main_character.y_velocity + GRAVITY < 0:
        main_character.y_velocity += GRAVITY
        sword.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.top + main_character.y_velocity < platform.rect.bottom < main_character.rect.top:
                    main_character.rect.top = platform.rect.bottom
                    main_character.y_velocity = 0
                    sword.y_velocity = 0
    else:
        main_character.y_velocity += GRAVITY
        sword.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left:
                if main_character.rect.bottom + main_character.y_velocity > platform.rect.top > main_character.rect.bottom:
                    main_character.rect.bottom = platform.rect.top
                    main_character.y_velocity = 0
                    sword.y_velocity = 0

    for platform in platform_group:
        platform.update()
    for character in character_group:
        character.update()
    sword.update()


def checkStanding(character):
    for platform in platform_group:
        if character.rect.bottom == platform.rect.top:
            if character.rect.left < platform.rect.right and character.rect.right > platform.rect.left:
                return True


def main():
    while True:
        DISPLAYSURF.fill((0, 0, 0))
        update_all()
        character_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)
        current_weapon.draw(DISPLAYSURF)

        # Event Loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    if checkStanding(main_character):
                        main_character.jump(sword)
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3) == (True, False, False):
                    sword.attacking = True



        # Update the Screen
        pygame.display.update()

        fpsClock.tick(FPS)

main()
