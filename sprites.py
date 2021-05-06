import pygame, sys

pygame.init()
import pygame
import os
import random
from pygame.sprite import *
from random import randint
infoObject = pygame.display.Info()

##################
# Character Classes
##################

# Main Character Class
class Character(pygame.sprite.Sprite):
    def __init__(self, sprites, posX, posY, health, damage, directionX, directionY, animationSpeed, gliding):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0

        if directionX != 0:
            # For when the sprite is reversed
            self.sprites1 = []
            for i in range(len(self.sprites)):
                self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))

        if infoObject.current_h == 720:
            for x in range(len(self.sprites)):
                self.sprites[x] = pygame.transform.scale(self.sprites[x], (int(self.sprites[x].get_width() * .667), int(self.sprites[x].get_height() * 0.667)))
            for x in range(len(self.sprites1)):
                self.sprites1[x] = pygame.transform.scale(self.sprites1[x], (int(self.sprites1[x].get_width() * 0.667), int(self.sprites1[x].get_height() * 0.667)))

        self.image = self.sprites[self.currentSprite]

        # position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.topleft = [posX, posY]
        self.gliding=gliding
        # Basic direction values for the character so that Andy can work on the weapons
        # These can be used as multipliers for speed when the character and other objects are moving
        self.directionX = directionX  # Can either be -1 or 1 (Left or Right)
        self.directionY = directionY  # Can either be -1, 0, or 1 (Down, Neutral, Up)

        #Character Health
        self.health = health
        #Character Damage on contact to player
        self.damage = damage
        self.animationSpeed = animationSpeed
        self.isMoving = False
        self.currentDirection = 1


    def update(self, direction, weapon1, weapon2):

        if self.isMoving:
            self.currentSprite += self.animationSpeed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0
        else:
            self.currentSprite = 0
        if weapon1.attacking == False:
            if direction == -1:
                self.image = self.sprites1[int(self.currentSprite)]
            else:
                self.image = self.sprites[int(self.currentSprite)]
        keys = pygame.key.get_pressed()
        self.currentDirection = direction
        if direction == -1 and weapon1.attacking == False:
            if weapon1.rect.left != weapon1.left2:
                weapon1.image = pygame.transform.flip(weapon1.originalImage, True, False)
                weapon1.rect.left = weapon1.left2
                weapon1.xDirection = -2
            if weapon2.rect.left != weapon2.left2:
                weapon2.image = weapon2.originalImage
                weapon2.image = pygame.transform.flip(weapon2.originalImage, True, False)
                weapon2.rect.left = weapon2.left2
                weapon2.rect.top = weapon2.height
                weapon2.xDirection = -2
                weapon2.yDirection = 0
            if keys[pygame.K_w]:
                if weapon2.rect.left != weapon2.left3:
                    weapon2.image = pygame.transform.rotate(weapon2.originalImage, 90)
                    weapon2.rect.left = weapon2.left3
                    weapon2.rect.top = weapon2.top1
                    weapon2.xDirection = 0
                    weapon2.yDirection = -2
            elif keys[pygame.K_s]:
                if weapon2.rect.left != weapon2.left3:
                    weapon2.image = pygame.transform.rotate(weapon2.originalImage, -90)
                    weapon2.image = pygame.transform.flip(weapon2.image, True, False)
                    weapon2.rect.left = weapon2.left3
                    weapon2.rect.top = weapon2.top2
                    weapon2.xDirection = 0
                    weapon2.yDirection = 2
        elif weapon1.attacking == False:
            if weapon1.rect.left != weapon1.left1:
                weapon1.image = weapon1.originalImage
                weapon1.rect.left = weapon1.left1
                weapon1.xDirection = 2
            if weapon2.rect.left != weapon2.left1:
                weapon2.image = weapon2.originalImage
                weapon2.image = weapon2.originalImage
                weapon2.rect.left = weapon2.left1
                weapon2.rect.top = weapon2.height
                weapon2.xDirection = 2
                weapon2.yDirection = 0
            if keys[pygame.K_w]:
                if weapon2.rect.left != weapon2.left4:
                    weapon2.image = pygame.transform.rotate(weapon2.originalImage, 90)
                    weapon2.image = pygame.transform.flip(weapon2.image, True, False)
                    weapon2.rect.left = weapon2.left4
                    weapon2.rect.top = weapon2.top1
                    weapon2.xDirection = 0
                    weapon2.yDirection = -2
            elif keys[pygame.K_s]:
                if weapon2.rect.left != weapon2.left4:
                    weapon2.image = pygame.transform.rotate(weapon2.originalImage, -90)
                    weapon2.rect.left = weapon2.left4
                    weapon2.rect.top = weapon2.top2
                    weapon2.xDirection = 0
                    weapon2.yDirection = 2







class MainCharacter(Character):
    def __init__(self, DISPLAYSURF):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load(os.path.join("Images", "Character0.png")))
        self.images.append(pygame.image.load(os.path.join("Images", "Character1.png")))
        self.images.append(pygame.image.load(os.path.join("Images", "Character2.png")))
        self.can_glide = False
        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_height = -18
        if infoObject.current_h == 720:
        #    self.jump_height = int(self.jump_height * .667)
            self.jump_height = -16
        self.can_double_jump = False
        self.gliding = False
        super().__init__(self.images, 0, 0, 10, 0, 1, 0, 0.25,self.gliding)
        self.health=100
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)
        self.maxhealth=100
        self.direction = 1
        self.jumped = False
        self.can_glide = False
        self.gliding = False

        self.invincibilityTime = 0
        self.isInvincible = False
        self.flashTicks = 0
        self.numberOfBoxes = 10
        self.timeTaken = 0


    def addmaxhealth(self):
        self.maxhealth+=10

    def update(self, weapon1, weapon2, ms):
        if infoObject.current_h == 720:
            self.x_velocity = int(self.x_velocity * 0.87)

        if self.x_velocity == 0 or self.y_velocity != 0:
            self.isMoving = False

        if self.isInvincible:
            if int((ms - self.timeTaken)/60) >= self.invincibilityTime:
                self.invincibilityTime = 0
                self.isInvincible = False
                self.flashTicks = 0

        super().update(self.direction, weapon1, weapon2)


    def addhealth(self):
        if self.health<self.maxhealth:
            self.health+=10
    def losehealth(self, damageTaken):
        if self.health>0:
            self.health -= damageTaken
    def activateGlide(self):
        self.can_glide = True
    def doubleJump(self):
        self.can_double_jump=True
    def hasDoubleJumped(self):
        return self.jumped
    def glide(self):
        self.gliding = True
    def displayhealth(self, DISPLAYSURF):
        for x in range(self.numberOfBoxes):
            color = (80, 80, 80)
            pygame.draw.rect(DISPLAYSURF, color, (10 + (x * 15), 10, 10, 10))
        if 30<self.health<60:
            tuple=(255,235,59)
        elif self.health<=30:
            tuple=(255,0,0)
        else:
            tuple=(0,255,0)
        i=0
        while i<self.health/10:
            pygame.draw.rect(DISPLAYSURF, tuple, (i*15+10, 10, 10, 10))
            i+=1

    def getShift(self):
        return self.x_velocity, self.y_velocity

    def jump(self, weapon):
        self.y_velocity = self.jump_height
        weapon.y_velocity = self.jump_height



##############
# Enemy Classes
##############
class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprites, posX, posY, health, damage, directionX, velocityX, velocityY, animationSpeed):
        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        if directionX != 0:
            # For when the sprite is reversed
            self.sprites1 = []
            for i in range(len(self.sprites)):
                self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))
        if infoObject.current_h == 720:
            for x in range(len(self.sprites)):
                self.sprites[x] = pygame.transform.scale(self.sprites[x], (int(self.sprites[x].get_width() * 0.667), int(self.sprites[x].get_height() * 0.667)))
            for x in range(len(self.sprites1)):
                self.sprites1[x] = pygame.transform.scale(self.sprites1[x], (int(self.sprites1[x].get_width() * 0.667), int(self.sprites1[x].get_height() * 0.667)))
        self.image = self.sprites[self.currentSprite]
        # position values
        self.rect = self.image.get_rect()

        self.posX = posX
        self.posY = posY
        self.rect.center = (self.posX, self.posY)

        self.health = health
        self.damage = damage

        self.animationSpeed = animationSpeed

        self.jumping = False
        self.jump_height = -1
        self.isJumping = False

        self.isBoss = False
        self.isAttacking = False

        #if infoObject.current_h == 720:
         #  self.jump_height = int(self.jump_height * 0.667)
        self.velocityX = velocityX
        self.velocityY = velocityY

        self.variationX = 1
        self.variationY = 1

        self.currentDirection = directionX

    def update(self, shiftX, shiftY):
        if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * .667)
            if self.velocityX != 0:
                self.velocityX = 2
        self.currentSprite += self.animationSpeed

        if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0


        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - (self.currentDirection * self.velocityX)
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)

    ##############
class BatEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        #self.images.append(pygame.image.load("Images/Bat.png"))
        self.images.append(pygame.image.load("Images/Bat1.png"))
        self.images.append(pygame.image.load("Images/Bat2.png"))
        self.images.append(pygame.image.load("Images/Bat3.png"))

        super().__init__(self.images, posX, posY, 20, 5, -1, 0, -4, 0.18)

class BugEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Bug1.png"))
        self.images.append(pygame.image.load("Images/Bug2.png"))


        super().__init__(self.images, posX, posY, 10, 10, -1, 4, 0, 0.25)

class ElephantEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        #self.images.append(pygame.image.load("Images/Elephant.png"))
        self.images.append(pygame.image.load("Images/Elephant1.png"))
        self.images.append(pygame.image.load("Images/Elephant2.png"))


        super().__init__(self.images, posX, posY, 50, 20, -1, 3, 0, 0.10)

class FrogEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/frog1.png"))
        self.images.append(pygame.image.load("Images/frog2.png"))


        super().__init__(self.images, posX, posY, 50, 15, -1, 0, 0, 0)
        if infoObject.current_h == 720:
            self.velocityX = self.velocityX - .5
        self.jumping = True
        self.jump_height = -16
        self.jump_distance = 5
        self.jumpIncrement = 0
        self.jumpIncrease = 0.01

    def update(self, shiftX, shiftY):

        if self.isJumping:
            self.currentSprite = 1
        else:
            self.currentSprite = 0



        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:

            self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - (self.currentDirection * self.velocityX)
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)

    def jump(self):
        self.isJumping = True
        self.velocityY = self.jump_height
        self.velocityX = self.jump_distance
        self.jumpIncrement = 0
        #if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * 0.667)


class MushroomEnemy(Enemy):
    def __init__(self, posX, posY):
        # Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Mushroom.png"))
        self.images.append(pygame.image.load("Images/Mushroom1.png"))
        self.images.append(pygame.image.load("Images/Mushroom2.png"))
        self.images.append(pygame.image.load("Images/Mushroom3.png"))


        super().__init__(self.images, posX, posY, 25, 5, -1, 0, 0, 0)
        if infoObject.current_h == 720:
            self.velocityX = self.velocityX - .5
        self.jumping = True
        self.jump_height = -16
        self.jump_distance = 4
        self.jumpIncrement = 0
        self.jumpIncrease = 0.05

    def update(self, shiftX, shiftY):
        if self.isJumping:
            self.currentSprite = 1
        else:
            self.currentSprite = 0

        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:

            self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - (self.currentDirection * self.velocityX)
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)


    def jump(self):
        self.isJumping = True
        self.velocityY = self.jump_height
        self.velocityX = self.jump_distance
        self.jumpIncrement = 0
        # if infoObject.current_h == 720:
        #   self.velocityY = int(self.velocityY * 0.667)

class RunningEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/RunningThing1.png"))
        self.images.append(pygame.image.load("Images/RunningThing2.png"))


        super().__init__(self.images, posX, posY, 50, 20, -1, 3, 0, 0.12)


#Bosses

class FrogBoss(Enemy):

    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Froggy1.png"))
        self.images.append(pygame.image.load("Images/Froggy2.png"))
        self.images.append(pygame.image.load("Images/Froggy3.png"))


        super().__init__(self.images, posX, posY, 1000, 8, -1, 0, 0, 0)
        if infoObject.current_h == 720:
            self.velocityX = self.velocityX - .5
        self.jumping = True
        self.jump_height = -20
        self.jump_distance = 20
        self.jumpIncrement = 0
        self.jumpIncrease = 0.015

        self.jumpCount = 0
        self.isBoss = True
        self.isAttacking = False
        self.time = 0
        self.largeDamage = 8
        self.smallDamage = 5
        self.spitAmount = 3
        self.hurt = False
        self.crazy = False
        self.activated = False
        self.slime = pygame.image.load("Images/Slimey.png")
        self.smallSlime = pygame.transform.scale(self.slime, (60, 60))
    def update(self, shiftX, shiftY):

        if self.isJumping:
            self.currentSprite = 1
        elif self.isAttacking:
            self.currentSprite = 2
        else:
            self.currentSprite = 0



        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:

            self.image = self.sprites[int(self.currentSprite)]
        self.rect.update(self.rect.left, self.rect.left, self.image.get_width(), self.image.get_height())
        self.posX -= shiftX - (self.currentDirection * self.velocityX)
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)
    def jump(self):
        self.isJumping = True
        self.velocityY = self.jump_height
        self.velocityX = self.jump_distance
        self.jumpIncrement = 0
        self.jumpCount += 1
    def attack(self, DISPLAYSURF, slimeBallGroup):
        if self.crazy == True:
            if self.currentDirection == 1:
                (spawnLeft, spawnTop) = self.rect.midright
            else:
                (spawnLeft, spawnTop) = self.rect.midleft
            image = self.slime
            damage = self.largeDamage
            speed = self.currentDirection
        else:
            tempCheck = int((random.random() * 3) + 1)
            if self.currentDirection == 1:
                if tempCheck == 1:
                    (spawnLeft, spawnTop) = self.rect.topright
                    spawnTop += 75
                elif tempCheck == 2:
                    (spawnLeft, spawnTop) = self.rect.midright
                    spawnTop += 15
                else:
                    (spawnLeft, spawnTop) = self.rect.bottomright
                    spawnTop -= 60
            else:
                if tempCheck == 1:
                    (spawnLeft, spawnTop) = self.rect.topleft
                    spawnTop += 75
                elif tempCheck == 2:
                    (spawnLeft, spawnTop) = self.rect.midleft
                    spawnTop += 15
                else:
                    (spawnLeft, spawnTop) = self.rect.bottomleft
                    spawnTop -= 60
            tempCheck = int((random.random() * 3) + 1)
            if tempCheck == 1:
                speed = self.currentDirection * 1.15
            elif tempCheck == 2:
                speed = self.currentDirection * 1.05
            elif tempCheck == 3:
                speed = self.currentDirection * .95
            else:
                speed = self.currentDirection
            image = self.smallSlime
            damage = self.smallDamage
        slimeBallGroup.add(SlimeBall(DISPLAYSURF, image, spawnLeft, spawnTop, speed, damage))

class BirdBoss(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Birdy1.png"))
        self.images.append(pygame.image.load("Images/Birdy2.png"))
        self.images.append(pygame.image.load("Images/Birdy3.png"))

        super().__init__(self.images, posX, posY, 800, 5, -1, 4, 4, 0.18)


        self.variationX = 1
        self.variationY = 1

        self.isBoss = True

        self.isInjured = False
        self.injuredCounter = 0

    def randomizeVariation(self):
        self.variationX = 1 + (randint(0, 100) / 25)
        self.variationY = 1 + (randint(0, 100) / 25)

    def update(self, shiftX, shiftY):
        if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * .667)
            if self.velocityX != 0:
                self.velocityX = 2
        self.currentSprite += self.animationSpeed

        if self.currentSprite >= 2:
            self.currentSprite = 0

        if self.isInjured:
            self.currentSprite = 2
            self.injuredCounter += 1
            if self.injuredCounter > 10:
                self.isInjured = False
                self.injuredCounter = 0



        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]


        if not self.isInjured:
            self.posX -= shiftX - int((self.currentDirection * self.velocityX) * self.variationX)
            self.posY -= shiftY - int(self.velocityY * self.variationY)
        else:
            self.posX -= shiftX
            self.posY -= shiftY

        self.rect.center = (self.posX, self.posY)

class SpinnyBoss(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/BigCircleThing1.png"))
        self.images.append(pygame.image.load("Images/BigCircleThing2.png"))
        self.images.append(pygame.image.load("Images/BigCircleThing3.png"))
        self.images.append(pygame.image.load("Images/BigCircleThing4.png"))
        self.images.append(pygame.image.load("Images/BigCircleThing5.png"))


        super().__init__(self.images, posX, posY, 2000, 10, 1, 1, 1, 0.18)

        self.velocity = 8

        self.isInjured = False
        self.injuredCounter = 0

        self.isBoss = True

        self.rotationCounter = 0
        self.goToCenter = False

        self.vulnerableTime = 900
        self.vCounter = 0

    def update(self, shiftX, shiftY):
        if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * .667)
            if self.velocityX != 0:
                self.velocityX = 2

        if self.vCounter == 0:
            self.currentSprite += self.animationSpeed
        else:
            self.currentSprite = 0

        if self.currentSprite >= len(self.sprites):
                self.currentSprite = 1

        self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - int(self.currentDirection * self.velocityX)
        self.posY -= shiftY - int(self.velocityY)

        self.rect.center = (self.posX, self.posY)

class SmallSpinnyBoiEnemy(Enemy):

    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/SmallCircleThing.png"))


        super().__init__(self.images, posX, posY, 10, 2, -1, randint(2, 4), randint(2, 4), 1)

        self.bounceCounter = 0

    def update(self, shiftX, shiftY):
        super().update(shiftX, shiftY)

        if self.bounceCounter > 7:
            self.kill()

##############
# Block Classes
##############

# Main Block Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, posX, posY, breakable, damage, walkthrough, hint):

        super().__init__()
        self.image = image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))

        # position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.center = (self.posX, self.posY)
        self.hint=hint
        # Object information
        self.health = 0
        self.breakable = breakable  # If True, destroy block in response to any damage
        self.damage = damage  # For Blocks such as spikes and lava, amount of damage inflicted to the player
        self.walkthrough = walkthrough

        self.collectable = False

    def update(self, shiftX, shiftY):
        self.posX -= shiftX
        self.posY -= shiftY
        self.rect.center = (self.posX, self.posY)


#Lower Block Classes
class BasicBlock(Platform):

    #  B

    def __init__(self, posX, posY):

        #Load Images
        self.sprite = pygame.image.load('Images/Grass.png')

        super().__init__(self.sprite, posX, posY, False, 0, False, False)
class Hint(Platform):

    #  B

    def __init__(self, posX, posY, stringNum, DISPLAYSURF):

        #Load Images
        self.sprite = pygame.image.load('Images/Hint.png')
        self.strings=['Press SPACE to jump', 'This is the double jump upgrade', 'This is the glide upgrade', 'Hold shift to glide while jumping', 'Watch out for falling blocks', 'Press E to change weapons', 'Press ENTER to attack', 'This adds health', 'This increases your max health', 'This upgrades the weapon in your hand', 'Press esc to end']
        super().__init__(self.sprite, posX, posY, False, 0, True, True)
        self.stringNum = stringNum
        self.DISPLAYSURF=DISPLAYSURF
    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            #pygame.draw.rect(self.DISPLAYSURF, (255,255,255), (self.DISPLAYSURF.get_wid/2,0,500,500) )
            fontObj = pygame.font.Font('freesansbold.ttf', 50)
            textSurfaceObj = fontObj.render(self.strings[self.stringNum], True, (255, 255, 255))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (int(self.DISPLAYSURF.get_width()/2+120), int(self.DISPLAYSURF.get_height()/2-240))
            self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
class Dirt(Platform):

    #  B

    def __init__(self, posX, posY):

        #Load Images
        self.sprite = pygame.image.load('Images/Dirt.png')

        super().__init__(self.sprite, posX, posY, False, 0, False, False)

class BreakableBlock(Platform):

    #  C

    def __init__(self, posX, posY):
        # Load Images
        self.sprite = pygame.image.load('Images/AnotherBlock.png')

        super().__init__(self.sprite, posX, posY, True, 0, False, False)

        self.health = 1

class Rock(Platform):

    #  R

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/BreakableBlock.png')

        super().__init__(self.sprite, posX, posY, False, 0, False, False)

class SpikesBlock(Platform):

    #  S

    def __init__(self, posX, posY):
        # Load Images
        self.sprite = pygame.image.load('Images/Spikes.png')

        super().__init__(self.sprite, posX, posY, False, 5, True, False)

class LavaBlock(Platform):

    #  L

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 10, True, False)


class SmashyBlock(Platform):

    #  O

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = []
        self.sprite.append(pygame.image.load('Images/Smashy0.png'))
        self.sprite.append(pygame.image.load('Images/Smashy1.png'))
        self.sprite.append(pygame.image.load('Images/Smashy2.png'))

        super().__init__(self.sprite[0], posX, posY, True, 100, False, False)
        if infoObject.current_h == 720:
            for x in range(3):
                self.sprite[x] = pygame.transform.scale(self.sprite[x], (int(self.sprite[x].get_width() * .667), int(self.sprite[x].get_height() * 0.667)))
        self.currentSprite = 0
        self.velocityY = 0
        self.isFalling = False
        self.hasFallen = False

        self.health = 50

    def update(self, shiftX, shiftY):

        if not self.hasFallen:
            if self.isFalling and self.currentSprite < 2:
                self.currentSprite += 0.5
        else:
            if self.currentSprite > 0:
                self.currentSprite -= 0.5

        self.image = self.sprite[int(self.currentSprite)]

        self.posX -= shiftX
        self.posY -= shiftY - self.velocityY


        self.rect.center = (self.posX, self.posY)

class InvisibleBlock(Platform):

    #  I

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/InvisibleBlock.png')


        super().__init__(self.sprite, posX, posY, False, 0, True, False)

class Collectables(Platform):
    def __init__(self, name, xpos, ypos, image, isWeaponUpgrade):

        self.name = name

        super().__init__(image, xpos, ypos, False, 0, True, False)

        self.collectable = True
        self.weaponUpgrade = isWeaponUpgrade


    def getname(self):
        return self.name

    def updatepos(self, x, y):
        self.posx = x
        self.posy = y

    def getposx(self):
        return self.posx

    def getposy(self):
        return self.posy


class DoubleUpgrade(Collectables):

    # J

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/DoubleJump.png')

        super().__init__("doublejump", xpos, ypos, image, False)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            char.doubleJump()
class WeaponUpgrade(Collectables):

    # W

    def __init__(self, xpos, ypos):
        image = pygame.image.load('Images/WeaponUpgrade.png')

        super().__init__("weaponupgrade", xpos, ypos, image, True)

    def is_collided_with(self, char, weapon):
        if self.rect.colliderect(char.rect):
            self.kill()
            weapon.upgradeCount -= 1

class Glide(Collectables):
    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/Glide.png')

        super().__init__("glide", xpos, ypos, image, False)

    def is_collided_with(self, char):
        self.kill()
        char.activateGlide()

class MaxHealth(Collectables):

    # J

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/MaxHealth.png')

        super().__init__("maxhealth", xpos, ypos, image, False)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            char.addmaxhealth()
            char.addhealth()
            char.numberOfBoxes += 1

class AddHealth(Collectables):

    # A

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/Health.png')

        super().__init__("health", xpos, ypos, image, False)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            char.addhealth()


##############
#Weapons
##############
class Sword(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.originalImage = _image
        self.isSword = True
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
            self.originalImage = pygame.transform.scale(self.originalImage, (int(self.originalImage.get_width() * 0.667), int(self.originalImage.get_height() * 0.667)))
        self.rect = self.image.get_rect()
        self.y_velocity = 0
        self.xDirection = 4
        self.attacking = False
        self.attackingCount = 8
        self.swordDamage = 8
        self.left1 = int(DISPLAYSURF.get_width() / 2) + 20
        self.left2 = int(DISPLAYSURF.get_width() / 2) - 36
        if infoObject.current_h != 720:
            self.left1 = int((DISPLAYSURF.get_width() / 2) + (22*1.4))
            self.left2 = int((DISPLAYSURF.get_width() / 2) - (38*1.45))
        self.height = int(DISPLAYSURF.get_height() / 2) + (14)
        if infoObject.current_h != 720:
            self.height =int((DISPLAYSURF.get_height()/2) + (14*1.4))
        self.rect.update(self.left1, self.height, self.rect.width, self.rect.height)
        self.upgradeCount = 10
        self.swordNumber = 0
        self.levelObj = pygame.font.Font('freesansbold.ttf', 13)
    def attack(self, enemyGroup, platformGroup):
        if self.attacking == True:
            self.rect.x = self.rect.x + self.xDirection
            self.attackingCount -= 1
            if self.attackingCount == 0:
                self.attacking = False
                self.attackingCount = 8
                self.xDirection = self.xDirection * -1
            elif self.attackingCount == 4:
                self.xDirection = self.xDirection * -1

            #Check Enemy damage
            spriteGroup = spritecollide(self, enemyGroup, False)
            for x in range(len(spriteGroup)):
                if isinstance(spriteGroup[x], SpinnyBoss):
                    if spriteGroup[x].currentSprite == 0:
                        spriteGroup[x].health -= self.swordDamage
                else:
                    spriteGroup[x].health -= self.swordDamage
                if isinstance(spriteGroup[x], BirdBoss):
                      spriteGroup[x].isInjured = True
                if isinstance(spriteGroup[x], FrogBoss):
                    if spriteGroup[x].isAttacking == True and spriteGroup[x].crazy == False and spriteGroup[x].hurt == False:
                        spriteGroup[x].hurt = True
                        spriteGroup[x].health -= self.swordDamage
                else:
                    spriteGroup[x].health -= self.swordDamage
                
                if spriteGroup[x].health <= 0:
                    randomNum = randint(1, 5)
                    if randomNum == 1:
                        platformGroup.add(AddHealth(spriteGroup[x].posX, spriteGroup[x].posY))
                    elif randomNum < 4:
                        platformGroup.add(WeaponUpgrade(spriteGroup[x].posX, spriteGroup[x].posY))

                    spriteGroup[x].kill()

            #Check Destructable platform damage
            spriteGroup = spritecollide(self, platformGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup[x].breakable:
                    spriteGroup[x].health -= self.swordDamage
                    if spriteGroup[x].health <= 0:
                        spriteGroup[x].kill()
    def update(self):
        if self.upgradeCount <= 0 and self.swordNumber < 2:
            self.swordNumber += 1
            self.swordDamage += 5
            self.image = pygame.image.load("Images/Sword" + str(self.swordNumber) + ".png")
            self.originalImage = pygame.image.load("Images/Sword" + str(self.swordNumber) + ".png")
            if infoObject.current_h == 720:
                self.left2 -= 5
                self.image = pygame.transform.scale(self.image, (
                    int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
                self.originalImage = pygame.transform.scale(self.originalImage, (
                    int(self.originalImage.get_width() * 0.667),
                    int(self.originalImage.get_height() * 0.667)))
            else:
                self.left2 -= 9
            self.upgradeCount = 10
    def displayPoints(self, DISPLAYSURF):
        for x in range(10):
            if x < 10 - self.upgradeCount:
                color = (185, 246, 202)
            else:
                color = (80,80,80)
            pygame.draw.rect(DISPLAYSURF, color, (10 + (x*15), 25, 10, 10))

        levelSurfaceObj = self.levelObj.render("Weapon Level: " + str(self.swordNumber + 1), True, (255, 255, 255))
        DISPLAYSURF.blit(levelSurfaceObj, (10, 40))

class SlimeBall(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image, left, top, directionx, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
        self.rect = self.image.get_rect()
        self.left = left
        self.height = top
        self.rect.center = (self.left, self.height)
        self.directionx = directionx
        self.damage = damage
    def move(self, platformGroup, player, shiftX, shiftY):
        self.rect.centerx -= shiftX
        self.rect.centery -= shiftY
        self.rect.centerx += (self.directionx * 10)
        spriteGroup = spritecollide(self, platformGroup, False)
        if pygame.sprite.spritecollideany(self, platformGroup) and spriteGroup[0].walkthrough == False:
            self.remove(self.groups())



class Bullet(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image, left, top, directionx, directiony, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
        self.rect = self.image.get_rect()
        self.left = left
        #if infoObject.current_h != 720:
         #   self.left = int(DISPLAYSURF.get_width() / 2) + (20*1.4)
        self.height = top
        #if infoObject.current_h != 720:
         #   self.height =int(DISPLAYSURF.get_height()/2) + (14*1.4)
        self.rect.center = (self.left, top)
        self.directionx = directionx
        self.directiony = directiony
        self.damage = damage
        if directiony > 1:
            self.movementCount = int(DISPLAYSURF.get_height() / 2)
        else:
            self.movementCount = int(DISPLAYSURF.get_width()/2)
    def move(self, platformGroup, enemyGroup, shiftX, shiftY):
        self.rect.centerx -= shiftX
        self.rect.centery -= shiftY
        self.rect.centerx += (self.directionx * 10)
        self.rect.centery += (self.directiony * 10)
        self.movementCount -= 1
        spriteGroup = spritecollide(self, platformGroup, False)
        if pygame.sprite.spritecollideany(self, platformGroup) and spriteGroup[0].walkthrough == False:
            self.remove(self.groups())
            spriteGroup = spritecollide(self, platformGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup[x].breakable:
                    spriteGroup[x].health -= self.damage
                    if spriteGroup[x].health <= 0:
                        spriteGroup[x].kill()

        #check enemy collisions
        if pygame.sprite.spritecollideany(self, enemyGroup):
            spriteGroup = spritecollide(self, enemyGroup, False)
            for x in range(len(spriteGroup)):
                if isinstance(spriteGroup[x], SpinnyBoss):
                    if spriteGroup[x].currentSprite == 0:
                        spriteGroup[x].health -= self.damage
                else:
                    spriteGroup[x].health -= self.damage
                if isinstance(spriteGroup[x], BirdBoss):
                    spriteGroup[x].isInjured = True
                if isinstance(spriteGroup[x], FrogBoss):
                    if spriteGroup[x].isAttacking == True and spriteGroup[x].crazy == False:
                        spriteGroup[x].hurt = True
                        spriteGroup[x].health -= self.damage
                else:
                    spriteGroup[x].health -= self.damage

                if spriteGroup[x].health <= 0:
                    randomNum = randint(1, 5)
                    if randomNum == 1:
                        platformGroup.add(AddHealth(spriteGroup[x].posX, spriteGroup[x].posY))
                    elif randomNum < 4:
                        platformGroup.add(WeaponUpgrade(spriteGroup[x].posX, spriteGroup[x].posY))

                    spriteGroup[x].kill()
            self.remove(self.groups())
        if self.movementCount <= 0:
            self.kill()
class Gun(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.originalImage = _image
        self.isSword = False
        self.xDirection = 2
        self.yDirection = 0
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
            self.originalImage = pygame.transform.scale(self.originalImage, (
            int(self.originalImage.get_width() * 0.667),
            int(self.originalImage.get_height() * 0.667)))
        self.rect = self.image.get_rect()
        self.gunDamage = 10
        self.left1 = int(DISPLAYSURF.get_width() / 2) - 13
        self.left2 = int(DISPLAYSURF.get_width() / 2) - 31
        self.left3 = int(DISPLAYSURF.get_width() / 2) - 26
        self.left4 = int(DISPLAYSURF.get_width() / 2) + 18
        self.top1 = int(DISPLAYSURF.get_height() / 2) - 15
        self.top2 = int(DISPLAYSURF.get_height() / 2) - 3
        if infoObject.current_h != 720:
            self.left1 = int((DISPLAYSURF.get_width() / 2) - (17 * 1.4))
            self.left2 = int((DISPLAYSURF.get_width() / 2) - (36 * 1.45))
            self.left3 = int((DISPLAYSURF.get_width() / 2) - (26 * 1.45))
            self.left4 = int((DISPLAYSURF.get_width() / 2) + (17 * 1.45))
            self.top1 = int((DISPLAYSURF.get_height() / 2) - (15 * 1.45))
        self.height = int((DISPLAYSURF.get_height() / 2) + (14))
        if infoObject.current_h != 720:
            self.height = int((DISPLAYSURF.get_height() / 2) + (14 * 1.4))
        self.rect.update(self.left1, self.height, self.rect.width, self.rect.height)
        self.canAttack = True
        self.shootTime = 360
        self.upgradeCount = 10
        self.gunNumber = 0
        self.levelObj = pygame.font.Font('freesansbold.ttf', 13)
    def attack(self, bulletGroup, DISPLAYSURF):
        if self.canAttack == True:
            if self.rect.left == self.left1:
                (spawnLeft, spawnTop) = self.rect.midright
                spawnTop -= 7
            elif self.rect.left == self.left2:
                (spawnLeft, spawnTop) = self.rect.midleft
                spawnTop -= 7
            elif self.rect.left == self.left3:
                if self.yDirection > 0:
                    (spawnLeft, spawnTop) = self.rect.midleft
                    spawnLeft += 4
                    spawnTop += 40
                elif self.yDirection < 0:
                    (spawnLeft, spawnTop) = self.rect.midleft
            elif self.rect.left == self.left4:
                if self.yDirection > 0:
                    (spawnLeft, spawnTop) = self.rect.midleft
                    spawnLeft += 12
                    spawnTop += 40
                elif self.yDirection < 0:
                    (spawnLeft, spawnTop) = self.rect.midbottom
                    spawnLeft -= 18
            bulletGroup.add(Bullet(DISPLAYSURF, pygame.image.load("Images/Bullet.png"), spawnLeft, spawnTop, self.xDirection, self.yDirection, self.gunDamage))
            self.canAttack = False
    def update(self):
        if self.upgradeCount <= 0 and self.gunNumber < 2:
            self.gunNumber += 1
            self.gunDamage += 10
            self.shootTime -= 150
            self.image = pygame.image.load("Images/Gun" + str(self.gunNumber) + ".png")
            self.originalImage = pygame.image.load("Images/Gun" + str(self.gunNumber) + ".png")
            if infoObject.current_h == 720:
                self.image = pygame.transform.scale(self.image, (
                    int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
                self.originalImage = pygame.transform.scale(self.originalImage, (
                    int(self.originalImage.get_width() * 0.667),
                    int(self.originalImage.get_height() * 0.667)))
            self.upgradeCount = 10
    def displayPoints(self, DISPLAYSURF):
        for x in range(10):
            if x < 10 - self.upgradeCount:
                color = (185, 246, 202)
            else:
                color = (80, 80, 80)
            pygame.draw.rect(DISPLAYSURF, color, (10 + (x * 15), 25, 10, 10))
        levelSurfaceObj = self.levelObj.render("Weapon Level: " + str(self.gunNumber + 1), True, (255, 255, 255))
        DISPLAYSURF.blit(levelSurfaceObj, (10, 40))

class Parachute(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.xcenter=WIDTH/2+8
        self.ycenter=HEIGHT/2-10
        self.originalImage = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * .667), int(self.image.get_height() * 0.667)))
            self.originalImage = pygame.transform.scale(self.image,(int(self.originalImage.get_width() * .667), int(self.originalImage.get_height() * 0.667)))
            self.xcenter += 4
            self.ycenter += 4
        self.rect = self.image.get_rect()
        self.rect.center=(self.xcenter, self.ycenter)
    def update(self, direction):
        if direction == -1:
            self.image= pygame.transform.flip(self.originalImage, True, False)
            self.rect.center = (self.xcenter-16, self.ycenter)
        else:
            self.image = self.originalImage
            if infoObject.current_h == 720:
                self.rect.center = (self.xcenter - 6, self.ycenter)
            else:
                self.rect.center = (self.xcenter, self.ycenter)


