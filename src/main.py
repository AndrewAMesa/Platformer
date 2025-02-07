import sys
import pygame, asyncio
from pygame.locals import *
from sprites import *


pygame.init()
fpsClock = pygame.time.Clock()

##############
# Image
##############
sword_image = pygame.image.load("Images/Sword0.png")
gun_image = pygame.image.load("Images/Gun0.png")
TILESIZE = 120
FPS = 60
GRAVITY = 1

if infoObject.current_h == 720:
 #   GRAVITY = GRAVITY * 0.667
    TILESIZE = 80
    sword_image = pygame.transform.scale(sword_image, (
        int(sword_image.get_width() * 0.667), int(sword_image.get_height() * 0.667)))
    gun_image = pygame.transform.scale(gun_image, (
        int(gun_image.get_width() * 0.667),
        int(gun_image.get_height() * 0.667)))
infoObject = pygame.display.Info()
DISPLAYSURF = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

platform_group = pygame.sprite.Group()
hint_group=pygame.sprite.Group()

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
slimeBallGroup = pygame.sprite.Group()

clockObj = pygame.font.Font('freesansbold.ttf', 20)
timeLeft = 500


def display_time(milliseconds):
    clockSurfaceObj = clockObj.render("TimeLeft: " + str(timeLeft - int(milliseconds / 60)), True, (255, 255, 255))
    DISPLAYSURF.blit(clockSurfaceObj, (DISPLAYSURF.get_width() - 143, 10))


def enemyMovement():
    for enemy in enemy_group:
        if isinstance(enemy, BatEnemy) or isinstance(enemy, BugEnemy) or isinstance(enemy, BirdBoss) or isinstance(enemy, SpinnyBoss) or isinstance(enemy, SmallSpinnyBoiEnemy) or isinstance(enemy, FrogBoss):
            for platform in platform_group:
                if enemy.velocityY < 0:
                    if enemy.rect.left + enemy.velocityX * enemy.variationX < platform.rect.right and enemy.rect.right + enemy.velocityX * enemy.variationX > platform.rect.left:
                        if enemy.rect.top + enemy.velocityY * enemy.variationY <= platform.rect.bottom <= enemy.rect.top and not platform.walkthrough:
                            enemy.velocityY *= -1
                            if isinstance(enemy, BirdBoss):
                                enemy.randomizeVariation()
                            if isinstance(enemy, SpinnyBoss):
                                if not enemy.goToCenter:
                                    enemy.velocityX = enemy.velocity
                                    enemy.velocityY = 0
                                    enemy.rotationCounter += 1
                                    enemy_group.add(SmallSpinnyBoiEnemy(enemy.posX, enemy.posY))
                            if isinstance(enemy, SmallSpinnyBoiEnemy):
                                enemy.bounceCounter += 1

                if enemy.velocityY > 0:
                    if enemy.rect.left + enemy.velocityX * enemy.variationX < platform.rect.right and enemy.rect.right + enemy.velocityX * enemy.variationX > platform.rect.left:
                        if enemy.rect.bottom + enemy.velocityY * enemy.variationY >= platform.rect.top >= enemy.rect.bottom and not platform.walkthrough:
                            enemy.velocityY *= -1
                            if isinstance(enemy, BirdBoss):
                                enemy.randomizeVariation()
                            if isinstance(enemy, SpinnyBoss):
                                if not enemy.goToCenter:
                                    enemy.velocityX = enemy.velocity
                                    enemy.velocityY = 0
                                    enemy_group.add(SmallSpinnyBoiEnemy(enemy.posX, enemy.posY))
                            if isinstance(enemy, SmallSpinnyBoiEnemy):
                                enemy.bounceCounter += 1
                if isinstance(enemy, SpinnyBoss) and isinstance(platform, InvisibleBlock):
                    if enemy.rotationCounter > 2 and not enemy.goToCenter:
                        if platform.posX - 5 <= enemy.posX <= platform.posX + 5:
                            enemy.rotationCounter = 0
                            enemy.velocityX = 0
                            enemy.velocityY = 6
                            enemy.goToCenter = True
                    if enemy.goToCenter:
                        enemy.vCounter += 1
                        if enemy.vCounter > enemy.vulnerableTime:
                            enemy.goToCenter = False
                            enemy.vCounter = 0
        if isinstance(enemy, FrogBoss):
            dirvect = pygame.math.Vector2(enemy.rect.centerx - main_character.rect.centerx, enemy.rect.centery - main_character.rect.centery)
            if (abs(dirvect.x) <= int(DISPLAYSURF.get_width()/2) and abs(dirvect.y) <= int(DISPLAYSURF.get_height()/2)) or enemy.activated == True:
                enemy.activated = True
                if enemy.crazy == True and enemy.isJumping == False:
                    enemy.time += fpsClock.tick_busy_loop(560)
                    if (enemy.time / 60) >= .7 and enemy.spitAmount > 0:
                        enemy.attack(DISPLAYSURF, slimeBallGroup)
                        enemy.time = 0
                        enemy.spitAmount -= 1
                        if enemy.spitAmount == 3:
                            enemy.currentDirection = enemy.currentDirection*-1
                    if enemy.spitAmount <= 0:
                        enemy.spitAmount = 3
                        enemy.time = 0
                        enemy.isAttacking = False
                        enemy.jumpCount = 0
                        enemy.jump()
                        enemy.crazy = False
                        enemy.hurt = False
                elif enemy.jumpCount >= 3 and enemy.isJumping == False:
                    dirvect = pygame.math.Vector2(int(DISPLAYSURF.get_width()/2) - enemy.rect.x, DISPLAYSURF.get_height()/2 - enemy.rect.y)
                    if dirvect.x < 0:
                        enemy.currentDirection = -1
                    elif dirvect.x > 0:
                        enemy.currentDirection = 1
                    enemy.time += fpsClock.tick_busy_loop(560)
                    if (enemy.time/60) > 1 and enemy.isAttacking == False:
                        enemy.time = 0
                        enemy.isAttacking = True
                    if enemy.isAttacking == True:
                        enemy.time += fpsClock.tick_busy_loop(560)
                        if (enemy.time/60) > 1 and enemy.spitAmount > 0:
                            enemy.attack(DISPLAYSURF, slimeBallGroup)
                            enemy.time = 0
                            enemy.spitAmount -= 1
                        if enemy.spitAmount <= 0:
                            if (enemy.time/60) > 7:
                                enemy.spitAmount = 3
                                enemy.time = 0
                                enemy.isAttacking = False
                                enemy.jumpCount = 0
                                enemy.jump()
                                if enemy.hurt == True:
                                    enemy.crazy = True
                                    enemy.isAttacking = True
                                    enemy.spitAmount = 6
                elif int(enemy.jumpIncrement) >= 1:
                    enemy.jump()
                else:
                    enemy.jumpIncrement += enemy.jumpIncrease
        if enemy.velocityX != 0:
            for platform in platform_group:
                if enemy.rect.bottom + enemy.velocityY * enemy.variationY > platform.rect.top and enemy.rect.top + enemy.velocityY * enemy.variationY < platform.rect.bottom:
                    if enemy.currentDirection > 0:
                        if enemy.rect.right + (
                                enemy.currentDirection * enemy.velocityX * enemy.variationX) >= platform.rect.left >= enemy.rect.right and not platform.walkthrough:
                            enemy.currentDirection *= -1
                            if isinstance(enemy, BirdBoss):
                                enemy.randomizeVariation()
                            if isinstance(enemy, SpinnyBoss):
                                if not enemy.goToCenter:
                                    enemy.velocityX = 0
                                    enemy.velocityY = -enemy.velocity
                            if isinstance(enemy, SmallSpinnyBoiEnemy):
                                enemy.bounceCounter += 1
                            if isinstance(enemy, FrogEnemy):
                                if enemy.rect.left + (
                                        enemy.velocityX * enemy.variationX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                                    enemy.currentDirection *= -1
                    if enemy.currentDirection < 0:
                        if enemy.rect.left + (
                                enemy.currentDirection * enemy.velocityX * enemy.variationX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                            enemy.currentDirection *= -1
                            if isinstance(enemy, BirdBoss):
                                enemy.randomizeVariation()
                            if isinstance(enemy, SpinnyBoss):
                                if not enemy.goToCenter:
                                    enemy.velocityX = 0
                                    enemy.velocityY = enemy.velocity
                            if isinstance(enemy, SmallSpinnyBoiEnemy):
                                enemy.bounceCounter += 1
                            if isinstance(enemy, FrogEnemy):
                                if enemy.rect.left + (
                                        enemy.velocityX * enemy.variationX) <= platform.rect.right <= enemy.rect.left and not platform.walkthrough:
                                    enemy.currentDirection *= -1
        if enemy.jumping and not enemy.isAttacking:
            if not enemy.isJumping and int(enemy.jumpIncrement) >= 1 and enemy.isBoss == False:
                enemy.jump()
            elif enemy.isBoss == False:
                enemy.jumpIncrement += enemy.jumpIncrease

        if isinstance(enemy, BirdBoss) and isinstance(platform, InvisibleBlock):
            collided_sprites = pygame.sprite.spritecollide(enemy, platform_group, False, collided=None)
            if len(collided_sprites) > 0:
                for i in range(len(collided_sprites)):
                    if isinstance(collided_sprites[i], InvisibleBlock):
                        enemy.kill()






def update_all():

    check_y_collisions()
    if current_weapon.sprites()[0].isSword == True:
        if current_weapon.sprites()[0].attacking == True:
            sword.attack(enemy_group, platform_group)
    character_group.update(sword, gun, milliseconds)
    shiftX, shiftY = main_character.getShift()
    enemyMovement()
    enemy_group.update(shiftX, shiftY)
    current_weapon.sprites()[0].update(main_character)


    #Falling Blocks
    for platform in platform_group:
        if isinstance(platform, SmashyBlock):
            if main_character.rect.left < platform.rect.right and main_character.rect.right > platform.rect.left and main_character.rect.centery > platform.rect.centery and not platform.isFalling and not platform.hasFallen:
                platform.velocityY = 10
                platform.isFalling = True
            if platform.isFalling:
                collided_sprites = pygame.sprite.spritecollide(platform, platform_group, False, collided=None)

                if len(collided_sprites) > 1 and not collided_sprites[1].walkthrough:
                    platform.velocityY = 0
                    platform.isFalling = False
                    platform.hasFallen = True
                    platform.posY = collided_sprites[1].posY - TILESIZE

    platform_group.update(shiftX, shiftY)
    spriteGroup = bullet_group.sprites()
    for x in range(len(spriteGroup)):
        spriteGroup[x].move(platform_group, enemy_group, shiftX, shiftY)
    ballSprites = slimeBallGroup.sprites()
    for x in range(len(ballSprites)):
        ballSprites[x].move(platform_group, main_character, shiftX, shiftY)


def checkcollision(char, group):
    collided_sprites = pygame.sprite.spritecollide(char, group, False, collided=None)
    for sprite in collided_sprites:
        if sprite.collectable:
            if sprite.weaponUpgrade == True:
                sprite.is_collided_with(char, current_weapon.sprites()[0])
            else:
                sprite.is_collided_with(char)
        elif sprite.hint:
            sprite.is_collided_with(char)

def damageCollision(char, group, milliseconds):
    collided_sprites = pygame.sprite.spritecollide(char, group, False, collided=None)
    for sprite in collided_sprites:
        if sprite.damage != 0:
            if not main_character.isInvincible:
                main_character.losehealth(sprite.damage)
                main_character.isInvincible = True
                main_character.invincibilityTime = 1
                main_character.timeTaken = milliseconds
                main_character.flashTicks = 0

def update_gun(milliseconds):
    if int(milliseconds / 60) >= 1 and gun.canAttack == False:
        gun.canAttack = True
        return 0
    else:
        return milliseconds




def check_y_collisions():
    #check enemy collisions
    for enemy in enemy_group:
        if not isinstance(enemy, BatEnemy) and not isinstance(enemy, BugEnemy) and not isinstance(enemy, BirdBoss) and not isinstance(enemy, SpinnyBoss) and not isinstance(enemy, SmallSpinnyBoiEnemy):
            if checkStanding(enemy) and enemy.velocityY != enemy.jump_height:
                enemy.velocityY = 0
                enemy.isJumping = False
                if isinstance(enemy, FrogEnemy) or isinstance(enemy, MushroomEnemy) or isinstance(enemy, FrogBoss):
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
                            if isinstance(enemy, FrogEnemy) or isinstance(enemy, MushroomEnemy) or isinstance(enemy, FrogBoss):
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
            if main_character.rect.bottom + main_character.y_velocity > platform.rect.top and main_character.rect.top + main_character.y_velocity < platform.rect.bottom:
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


async def main(levelNum):
    global milliseconds
    milliseconds = 0
    gunMilliseconds = 0
    readFile(levelNum)

    if levelNum == 1 or levelNum == 0:
        color = (0, 129, 129)
    elif levelNum == 2:
        color = (0, 71, 71)
    elif levelNum == 3:
        color = (90, 90, 90)

    lose = False
    win = False

    while not lose and not win:
        DISPLAYSURF.fill(color)
        update_all()
        checkcollision(main_character, platform_group)
        damageCollision(main_character, enemy_group, milliseconds)
        damageCollision(main_character, platform_group, milliseconds)
        damageCollision(main_character, slimeBallGroup, milliseconds)

        if not main_character.isInvincible:
            character_group.draw(DISPLAYSURF)
            current_weapon.draw(DISPLAYSURF)
        else:
            main_character.flashTicks += 1
        if main_character.flashTicks == 0 or main_character.flashTicks % 4 == 0:
            character_group.draw(DISPLAYSURF)
            current_weapon.draw(DISPLAYSURF)

        bullet_group.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        platform_group.draw(DISPLAYSURF)
        slimeBallGroup.draw(DISPLAYSURF)
        main_character.displayhealth(DISPLAYSURF)
        current_weapon.sprites()[0].displayPoints(DISPLAYSURF)
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
                if event.key == K_ESCAPE and sword.attacking == False:
                    win = True
                    lose = True

                if event.key == K_r and sword.attacking == False:
                    lose = True

                if event.key == K_SPACE:
                    if checkStanding(main_character):
                        main_character.jump(sword)
                    elif main_character.can_double_jump is True and main_character.hasDoubleJumped() is False:
                        main_character.jump(sword)
                        check_y_collisions()
                        main_character.jumped = True

                if event.key == K_RETURN:
                    if current_weapon.sprites()[0].isSword and main_character.health > 0:
                        current_weapon.sprites()[0].attacking = True
                    elif main_character.health > 0:
                        current_weapon.sprites()[0].attack(bullet_group, DISPLAYSURF)

                if event.key == K_e:
                    spriteArray = current_weapon.sprites()
                    if spriteArray[0].isSword:
                        current_weapon.remove(spriteArray[0])
                        current_weapon.add(gun)
                    else:
                        current_weapon.remove(spriteArray[0])
                        current_weapon.add(sword)

        if win and lose:
            break

        if main_character.health <= 0:
            lose = True

        if levelNum != 0 and sword.attacking == False:
            win = True
            for enemy in enemy_group:
                if enemy.isBoss:
                    win = False

        # Update the Screen
        if timeLeft - int(milliseconds / 60) <= 0:
            main_character.health = 0
        pygame.display.update()
        fpsClock.tick(FPS)
        milliseconds += fpsClock.tick_busy_loop(560)

        if not gun.canAttack:
            gunMilliseconds += fpsClock.tick_busy_loop(gun.shootTime)

        await asyncio.sleep(0)

    return win, lose


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

    stringNum = 0

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
            elif b[i][j] == "D":
                platform_group.add(Dirt((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "C":
                platform_group.add(BreakableBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "R":
                platform_group.add(Rock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "O":
                platform_group.add(SmashyBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "I":
                platform_group.add(InvisibleBlock((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "!":
                enemy_group.add(FrogBoss((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "?":
                platform_group.add(Hint((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize), stringNum, DISPLAYSURF))
                stringNum += 1
            elif b[i][j] == "@":
                enemy_group.add(BirdBoss((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))
            elif b[i][j] == "#":
                enemy_group.add(SpinnyBoss((int(SCREEN_WIDTH / 2) - (startingPosX - i) * shiftSize),
                                             (int(SCREEN_HEIGHT / 2) - (startingPosY - j) * shiftSize)))

async def menu():
    font = pygame.font.SysFont(None, 100)
    smallFont = pygame.font.SysFont(None, 50)
    pygame.event.clear(eventtype=KEYDOWN)

    mode = 0
    pos = 1
    showControls = False

    while mode == 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if showControls:
                        showControls = False
                    else:
                        pygame.quit()
                        sys.exit()

                if event.key == K_RETURN:
                    if not showControls:
                        if pos == 1:
                            mode = 1
                        elif pos == 2:
                            showControls = True
                        else:
                            mode = 2
                    else:
                        showControls = False

                if event.key == K_w and pos > 1:
                    pos -= 1
                if event.key == K_s and pos < 3:
                    pos += 1

        DISPLAYSURF.fill((69, 69, 69))
        if not showControls:
            img = font.render("GAME", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)

            img = smallFont.render("Play", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0),
                                 (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
            img = smallFont.render("Controls", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), 1.25 * int(SCREEN_HEIGHT / 2)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0),
                                 (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
            img = smallFont.render("Tutorial", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), 3 * int(SCREEN_HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 3:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0),
                                 (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
        else:
            img = smallFont.render(" - Controls - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Use the WASD keys to move", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Enter to use your weapon", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 2 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press E to change weapons", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 3 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Space to jump", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 4 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Shift in midair to glide", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2),
                        int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 5 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Escape to quit", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2),
                        int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 6 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press R to restart the level", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2),
                        int(SCREEN_HEIGHT / 4) + int(SCREEN_HEIGHT * 0.05) + 7 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)

            img = smallFont.render("Press Enter to return to the title screen", True, (255, 255, 255))
            imgPos = img.get_rect(
                center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4) + 3 * int(SCREEN_HEIGHT * 0.05) + 11 * int(SCREEN_HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)

        pygame.display.update()
        fpsClock.tick(FPS)

        # Yield control back to the event loop
        await asyncio.sleep(0)

    return mode

async def async_main():
    font = pygame.font.SysFont(None, 100)

    while True:
        mode = await menu()
        if mode == 1:
            levelNum = 1
            while levelNum < 4:
                win, lose = await main(levelNum)  # Use await here to call main asynchronously

                if lose and not win:
                    if levelNum == 1:
                        main_character.can_double_jump = False
                    elif levelNum == 2:
                        main_character.maxhealth = 100
                    elif levelNum == 3:
                        main_character.can_glide = False
                    main_character.health = main_character.maxhealth

                    waitTime = int(pygame.time.get_ticks() / 1000) + 2
                    while waitTime > int(pygame.time.get_ticks() / 1000):
                        img = font.render("You Died!", True, (255, 255, 255))
                        imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 3)))
                        DISPLAYSURF.blit(img, imgPos)
                        pygame.display.update()
                        await asyncio.sleep(0)  # Yield control to event loop

                if win and not lose:
                    waitTime = int(pygame.time.get_ticks() / 1000) + 2
                    while waitTime > int(pygame.time.get_ticks() / 1000):
                        if levelNum != 3:
                            img = font.render("You won level " + str(levelNum) + "!", True, (255, 255, 255))
                        else:
                            img = font.render("Congratulations, you beat the game!", True, (255, 255, 255))
                        imgPos = img.get_rect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 3)))
                        DISPLAYSURF.blit(img, imgPos)
                        pygame.display.update()
                        await asyncio.sleep(0)  # Yield control to event loop

                    levelNum += 1

                main_character.isInvincible = False
                enemy_group.empty()
                platform_group.empty()

                if win and lose:
                    break

            # Reset the character and game state
            main_character.can_double_jump = False
            main_character.maxhealth = 100
            main_character.can_glide = False
            main_character.direction = 1
            main_character.health = main_character.maxhealth
            main_character.isInvincible = False
            sword.upgradeCount = 10
            sword.swordNumber = 0
            sword.image = sword_image
            sword.originalImage = sword_image
            gun.image = gun_image
            gun.originalImage = gun_image
            gun.gunNumber = 0
            gun.gunDamage = 10
            sword.swordDamage = 8
            gun.upgradeCount = 10
            gun.shootTime = 360
            enemy_group.empty()
            platform_group.empty()

        elif mode == 2:
            await main(0)  # Call main asynchronously for mode 2 as well

            main_character.can_double_jump = False
            main_character.maxhealth = 100
            main_character.can_glide = False
            main_character.direction = 1
            main_character.health = main_character.maxhealth
            main_character.isInvincible = False
            sword.upgradeCount = 10
            sword.swordNumber = 0
            sword.image = sword_image
            sword.originalImage = sword_image
            gun.image = gun_image
            gun.originalImage = gun_image
            gun.gunNumber = 0
            gun.upgradeCount = 10
            gun.shootTime = 360
            gun.gunDamage = 10
            sword.swordDamage = 8
            enemy_group.empty()
            platform_group.empty()

if __name__ == '__main__':
    asyncio.run(async_main())

