import sys
import pygame
from pygame.locals import *
from sprites import *

pygame.init()
fpsClock = pygame.time.Clock()

##############
# Image
##############
sword_image = pygame.image.load("Images/Sword.png")
gun_image = pygame.image.load("Images/Gun.png")
TILESIZE = 30
FPS = 60
GRAVITY = 1

#if infoObject.current_h == 720:
 #   GRAVITY = GRAVITY * 0.667
infoObject = pygame.display.Info()
DISPLAYSURF = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

platform_group = pygame.sprite.Group()

sword = Sword(DISPLAYSURF, sword_image)
gun = Gun(DISPLAYSURF, gun_image)
current_weapon = pygame.sprite.Group()
current_weapon.add(sword)
bullet_group = pygame.sprite.Group()


main_character = MainCharacter(DISPLAYSURF)
character_group = pygame.sprite.Group()
character_group.add(main_character)

parachute=Parachute(SCREEN_WIDTH, SCREEN_HEIGHT, pygame.image.load('Images/Parachute.png'))
parachute_group=pygame.sprite.Group()
parachute_group.add(parachute)

enemy_group = pygame.sprite.Group()


clockObj = pygame.font.Font('freesansbold.ttf', 20)
timeLeft = 500


def display_time(milliseconds):
    clockSurfaceObj = clockObj.render("TimeLeft: " + str(timeLeft - int(milliseconds / 60)), True, (255, 255, 255))
    DISPLAYSURF.blit(clockSurfaceObj, (DISPLAYSURF.get_width() - 143, 10))


def enemyMovement():
    for enemy in enemy_group:
        if isinstance(enemy, BatEnemy) or isinstance(enemy, BugEnemy):
            for platform in platform_group:
                if enemy.velocityY < 0:
                    if enemy.rect.left + enemy.velocityX < platform.rect.right and enemy.rect.right + enemy.velocityX > platform.rect.left:
                        if enemy.rect.top + enemy.velocityY <= platform.rect.bottom <= enemy.rect.top and not platform.walkthrough:
                            enemy.velocityY *= -1
                if enemy.velocityY > 0:
                    if enemy.rect.left + enemy.velocityX < platform.rect.right and enemy.rect.right + enemy.velocityX > platform.rect.left:
                        if enemy.rect.bottom + enemy.velocityY >= platform.rect.top >= enemy.rect.bottom and not platform.walkthrough:
                            enemy.velocityY *= -1
        if enemy.velocityX != 0:
            for platform in platform_group:
                if enemy.rect.bottom > platform.rect.top and enemy.rect.top < platform.rect.bottom:
                    if enemy.currentDirection > 0:
                        if enemy.rect.right + (
                                enemy.currentDirection * enemy.velocityX) >= platform.rect.left >= enemy.rect.right and not platform.walkthrough:
                            enemy.currentDirection *= -1
                        if isinstance(enemy, FrogEnemy):
                            if enemy.rect.left + (enemy.velocityX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                                enemy.currentDirection *= -1
                    if enemy.currentDirection < 0:
                        if enemy.rect.left + (
                                enemy.currentDirection * enemy.velocityX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                            enemy.currentDirection *= -1
                        if isinstance(enemy, FrogEnemy):
                            if enemy.rect.left + (enemy.velocityX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                                enemy.currentDirection *= -1
        if enemy.jumping:
            if not enemy.isJumping and int(enemy.jumpIncrement) >= 1:
                enemy.jump()
            else:
                enemy.jumpIncrement += enemy.jumpIncrease




def update_all():
    spriteGroup = bullet_group.sprites()
    for x in range (len(spriteGroup)):
        spriteGroup[x].move(platform_group, enemy_group)
    check_y_collisions()
    sword.attack(enemy_group)
    character_group.update(sword, gun, milliseconds)
    shiftX, shiftY = main_character.getShift()
    enemyMovement()

    enemy_group.update(shiftX, shiftY)
    platform_group.update(shiftX, shiftY)



def checkcollision(char, group):
    collided_sprites = pygame.sprite.spritecollide(char, group, False, collided=None)
    for sprite in collided_sprites:
        if sprite.collectable:
            sprite.is_collided_with(char)

def damageCollision(char, group):
    collided_sprites = pygame.sprite.spritecollide(char, group, False, collided=None)
    for sprite in collided_sprites:
        if sprite.damage != 0:
            if not main_character.isInvincible:
                main_character.losehealth(sprite.damage)
                main_character.isInvincible = True
                main_character.invincibilityTime = 120

def update_gun(milliseconds):
    if int(milliseconds / 60) >= 1 and gun.canAttack == False:
        gun.canAttack = True
        return 0
    else:
        return milliseconds




def check_y_collisions():
    #check enemy collisions
    for enemy in enemy_group:
        if not isinstance(enemy, BatEnemy) and not isinstance(enemy, BugEnemy):
            if checkStanding(enemy) and enemy.velocityY != enemy.jump_height:
                enemy.velocityY = 0
                enemy.isJumping = False
                if isinstance(enemy, FrogEnemy) or isinstance(enemy, MushroomEnemy):
                    enemy.velocityX = 0
            elif enemy.velocityY + GRAVITY < 0:
                enemy.velocityY += GRAVITY
                for platform in platform_group:
                    if enemy.rect.left + enemy.velocityX < platform.rect.right and enemy.rect.right + enemy.velocityX > platform.rect.left:
                        if enemy.rect.top + enemy.velocityY <= platform.rect.bottom <= enemy.rect.top and not platform.walkthrough:
                            enemy.velocityY = 0

            else:
                enemy.velocityY += GRAVITY
                for platform in platform_group:
                    if enemy.rect.left + enemy.velocityX < platform.rect.right and enemy.rect.right + enemy.velocityX > platform.rect.left:
                        if enemy.rect.bottom + enemy.velocityY >= platform.rect.top >= enemy.rect.bottom and not platform.walkthrough:
                            enemy.velocityY = 0
                            if isinstance(enemy, FrogEnemy) or isinstance(enemy, MushroomEnemy):
                                enemy.velocityX = 0
                                enemy.isJumping = False
    #check character collisions
    if checkStanding(main_character) and main_character.y_velocity != main_character.jump_height:
        main_character.y_velocity = 0
    elif main_character.y_velocity + GRAVITY < 0:
        main_character.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left + main_character.x_velocity < platform.rect.right and main_character.rect.right + main_character.x_velocity > platform.rect.left:
                if main_character.rect.top + main_character.y_velocity <= platform.rect.bottom <= main_character.rect.top and not platform.walkthrough:
                    main_character.y_velocity = 0

    else:
        if main_character.gliding and main_character.y_velocity >= 3:
            main_character.y_velocity = 3
            sword.y_velocity += 3
            parachute_group.update(main_character.direction)
            parachute_group.draw(DISPLAYSURF)
        else:

            main_character.y_velocity += GRAVITY
            sword.y_velocity += GRAVITY
        for platform in platform_group:
            if main_character.rect.left + main_character.x_velocity < platform.rect.right and main_character.rect.right + main_character.x_velocity > platform.rect.left:
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
                character.jumped = False
                return True


def main():
    global milliseconds
    milliseconds = 0
    gunMilliseconds = 0
    readFile(0)

    lose = False
    win = False

    while not lose and not win:

        DISPLAYSURF.fill((0, 69, 69))
        update_all()
        checkcollision(main_character, platform_group)
        damageCollision(main_character, enemy_group)
        damageCollision(main_character, platform_group)
        character_group.draw(DISPLAYSURF)
        current_weapon.draw(DISPLAYSURF)
        bullet_group.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)
        main_character.displayhealth(DISPLAYSURF)
        display_time(milliseconds)
        gunMilliseconds = update_gun(gunMilliseconds)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            main_character.isMoving = True
            main_character.direction = 1
            main_character.x_velocity = 5
            if check_x_collisions() == "Right":
                main_character.x_velocity = 0
        elif keys[pygame.K_a]:
            main_character.isMoving = True
            main_character.direction = -1
            main_character.x_velocity = -5
            if check_x_collisions() == "Left":
                main_character.x_velocity = 0
        else:
            main_character.x_velocity = 0
        if keys[pygame.K_LSHIFT] and main_character.can_glide:
            main_character.gliding = True
        else:
            main_character.gliding = False
        # Event Loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if checkStanding(main_character):
                        main_character.jump(sword)
                    elif main_character.can_double_jump is True and main_character.hasDoubleJumped() is False:
                        main_character.jump(sword)
                        check_y_collisions()
                        main_character.jumped = True
                if event.key == K_RETURN:
                    if current_weapon.sprites()[0].isSword == True:
                        sword.attacking = True
                    else:
                        current_weapon.sprites()[0].attack(bullet_group, DISPLAYSURF)
                if event.key == K_e:
                    spriteArray = current_weapon.sprites()
                    if spriteArray[0].isSword == True:
                        current_weapon.remove(spriteArray[0])
                        current_weapon.add(gun)
                    else:
                        current_weapon.remove(spriteArray[0])
                        current_weapon.add(sword)


        #if main_character.health <= 0:
        #    lose = True

        # Update the Screen

        pygame.display.update()
        fpsClock.tick(FPS)
        milliseconds += fpsClock.tick_busy_loop(560)
        if gun.canAttack == False:
            gunMilliseconds += fpsClock.tick_busy_loop(660)


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
                platform_group.add(LavaBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "J":
                platform_group.add(DoubleUpgrade((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                                 (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "A":
                platform_group.add(AddHealth((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "M":
                platform_group.add(MaxHealth((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "S":
                platform_group.add(SpikesBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "G":
                platform_group.add(Glide((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "W":
                platform_group.add(WeaponUpgrade((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "a":
                enemy_group.add(BatEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "b":
                enemy_group.add(BugEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "c":
                enemy_group.add(ElephantEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "d":
                enemy_group.add(FrogEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "e":
                enemy_group.add(MushroomEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "f":
                enemy_group.add(RunningEnemy((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                               (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "B":
                platform_group.add(BasicBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "C":
                platform_group.add(BreakableBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "R":
                platform_group.add(Rock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
main()
