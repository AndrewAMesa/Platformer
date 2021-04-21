import pygame, sys

pygame.init()
import pygame
import os
from pygame.sprite import *
infoObject = pygame.display.Info()

##################
# Character Classes
##################

# Main Character Class
class Character(pygame.sprite.Sprite):
    def __init__(self, sprites, posX, posY, health, damage, directionX, directionY, animationSpeed):

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
        if direction == -1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]
        keys = pygame.key.get_pressed()
        if direction != self.currentDirection:
          self.currentDirection = direction
          if direction == -1:
              if weapon1.rect.left != weapon1.left2:
                  weapon1.image = pygame.transform.flip(weapon1.originalImage, True, False)
                  weapon1.rect.left = weapon1.left2
                  weapon1.xDirection = -2
                  weapon1.attacking = False
                  weapon2.image = weapon2.originalImage
                  weapon2.image = pygame.transform.flip(weapon2.originalImage, True, False)
                  weapon2.rect.left = weapon2.left2
                  weapon2.rect.top = weapon2.height
                  weapon2.xDirection = -2
                  weapon2.yDirection = 0


          else:
              if weapon1.rect.left != weapon1.left1:
                  weapon1.image = weapon1.originalImage
                  weapon1.rect.left = weapon1.left1
                  weapon1.xDirection = 2
                  weapon1.attacking = False
                  weapon2.image = weapon2.originalImage
                  weapon2.image = weapon2.originalImage
                  weapon2.rect.left = weapon2.left1
                  weapon2.rect.top = weapon2.height
                  weapon2.xDirection = 2
                  weapon2.yDirection = 0
        if direction == -1:
            if keys[pygame.K_w]:
                weapon2.image = pygame.transform.rotate(weapon2.originalImage, 90)
                weapon2.rect.left = weapon2.left3
                weapon2.rect.top = weapon2.top1
                weapon2.xDirection = 0
                weapon2.yDirection = -2
            elif keys[pygame.K_s]:
                weapon2.image = pygame.transform.rotate(weapon2.originalImage, -90)
                weapon2.image = pygame.transform.flip(weapon2.image, True, False)
                weapon2.rect.left = weapon2.left3
                weapon2.rect.top = weapon2.top2
                weapon2.xDirection = 0
                weapon2.yDirection = 2
        else:
            if keys[pygame.K_w]:
                weapon2.image = pygame.transform.rotate(weapon2.originalImage, 90)
                weapon2.image = pygame.transform.flip(weapon2.image, True, False)
                weapon2.rect.left = weapon2.left4
                weapon2.rect.top = weapon2.top1
                weapon2.xDirection = 0
                weapon2.yDirection = -2
            elif keys[pygame.K_s]:
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
        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_height = -18
        if infoObject.current_h == 720:
        #    self.jump_height = int(self.jump_height * .667)
            self.jump_height = -16
        self.can_double_jump = False
        super().__init__(self.images, 0, 0, 10, 0, 1, 0, 0.25)
        self.health=100
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)
        self.maxhealth=100
        self.direction = 1
        self.jumped = False
        self.can_glide = False
        self.gliding = False

    def addmaxhealth(self):
        self.maxhealth+=10

    def update(self, weapon1, weapon2):
        if infoObject.current_h == 720:
            self.x_velocity = int(self.x_velocity * 0.667)

        if self.x_velocity == 0 or self.y_velocity != 0:
            self.isMoving = False

        super().update(self.direction, weapon1, weapon2)


    def addhealth(self):
        if self.health<self.maxhealth:
            self.health+=10
    def losehealth(self):
        if self.health>0:
            self.health-=10
    def activateGlide(self):
        self.can_glide = True
    def doubleJump(self):
        self.can_double_jump=True
    def hasDoubleJumped(self):
        return self.jumped
    def glide(self):
        self.gliding = True
    def displayhealth(self, DISPLAYSURF):
        if 30<self.health<60:
            tuple=(255,235,59)
        elif self.health<30:
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

        #if infoObject.current_h == 720:
         #  self.jump_height = int(self.jump_height * 0.667)
        self.velocityX = velocityX
        self.velocityY = velocityY

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

        super().__init__(self.images, posX, posY, 20, 10, -1, 0, -4, 0.18)

class BugEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Bug1.png"))
        self.images.append(pygame.image.load("Images/Bug2.png"))


        super().__init__(self.images, posX, posY, 10, 10, -1, 0, 4, 0.25)

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


        super().__init__(self.images, posX, posY, 50, 20, -1, 0, 0, 0)

        self.jumping = True
        self.jump_height = -18
    def update(self, shiftX, shiftY):

        if self.isJumping:
            self.currentSprite = 1
        else:
            self.currentSprite = 0

        if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * .667)
            self.velocityX = int(self.velocityX * .667)

        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - self.velocityX
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)

    def jump(self):
        self.isJumping = True
        self.velocityY = self.jump_height
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


        super().__init__(self.images, posX, posY, 50, 20, -1, 0, 0, 0)

        self.jumping = True
        self.jump_height = -18


    def update(self, shiftX, shiftY):

        if self.isJumping:
            self.currentSprite = 1
        else:
            self.currentSprite = 0
        if infoObject.current_h == 720:
         #   self.velocityY = int(self.velocityY * .667)
            self.velocityX = int(self.velocityX * .667)
        if self.currentDirection == 1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]

        self.posX -= shiftX - self.velocityX
        self.posY -= shiftY - self.velocityY

        self.rect.center = (self.posX, self.posY)

    def jump(self):
        self.isJumping = True
        self.velocityY = self.jump_height
       # if infoObject.current_h == 720:
        #    self.velocityY = int(self.velocityY * 0.667)

class RunningEnemy(Enemy):
    def __init__(self, posX, posY):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/RunningThing1.png"))
        self.images.append(pygame.image.load("Images/RunningThing2.png"))


        super().__init__(self.images, posX, posY, 50, 20, -1, 3, 0, 0.12)
##############
# Block Classes
##############

# Main Block Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, posX, posY, breakable, damage, walkthrough):

        super().__init__()
        self.image = image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))

        # position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.center = (self.posX, self.posY)

        # Object information
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

        super().__init__(self.sprite, posX, posY, False, 0, False)

class BreakableBlock(Platform):

    #  C

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/BreakableBlock.png')

        super().__init__(self.sprite, posX, posY, True, 0, False)

class SpikesBlock(Platform):

    #  S

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Spikes.png')

        super().__init__(self.sprite, posX, posY, False, 5, True)

class LavaBlock(Platform):

    #  L

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 5, True)

class DoorBlock(Platform):

    #  D

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0, False)

class MovingBlock(Platform):

    #  D

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0, False)

class Collectables(Platform):
    def __init__(self, name, xpos, ypos, image):

        self.name = name

        super().__init__(image, xpos, ypos, False, 0, True)

        self.collectable = True

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

        super().__init__("doublejump", xpos, ypos, image)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            char.doubleJump()

class Glide(Collectables):
    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/Glide.png')

        super().__init__("glide", xpos, ypos, image)

    def is_collided_with(self, char):
        self.kill()
        char.activateGlide()

class MaxHealth(Collectables):

    # J

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/MaxHealth.png')

        super().__init__("maxhealth", xpos, ypos, image)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            char.addmaxhealth()
            char.addhealth()

class AddHealth(Collectables):

    # A

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/Health.png')

        super().__init__("health", xpos, ypos, image)

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
        self.xDirection = 2
        self.attacking = False
        self.attackingCount = 8
        self.swordDamage = 10
        self.left1 = int(DISPLAYSURF.get_width() / 2) + 20
        self.left2 = int(DISPLAYSURF.get_width() / 2) - 36
        if infoObject.current_h != 720:
            self.left1 = int(DISPLAYSURF.get_width() / 2) + (20*1.4)
            self.left2 = int(DISPLAYSURF.get_width() / 2) - (36*1.45)
        self.height = int(DISPLAYSURF.get_height() / 2) + (14)
        if infoObject.current_h != 720:
            self.height =int(DISPLAYSURF.get_height()/2) + (14*1.4)
        self.rect.update(self.left1, self.height, self.rect.width, self.rect.height)

    def attack(self, enemyGroup):
        if self.attacking == True:
            self.rect.x += self.xDirection
            self.attackingCount -= 1
            if self.attackingCount == 0:
                self.attacking = False
                self.attackingCount = 8
                self.xDirection = self.xDirection * -1
            elif self.attackingCount == 4:
                self.xDirection = self.xDirection * -1
            spriteGroup = spritecollide(self, enemyGroup, False)
            for x in range(len(spriteGroup)):
                spriteGroup[x].health -= self.swordDamage
                if spriteGroup[x].health <= 0:
                    spriteGroup[x].kill()
class Bullet(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image, left, top, directionx, directiony, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.667), int(self.image.get_height() * 0.667)))
        self.rect = self.image.get_rect()
        self.left = left
        if infoObject.current_h != 720:
            self.left = int(DISPLAYSURF.get_width() / 2) + (20*1.4)
        self.height = top
        if infoObject.current_h != 720:
            self.height =int(DISPLAYSURF.get_height()/2) + (14*1.4)
        self.rect.update(self.left, self.height, self.rect.width, self.rect.height)
        self.directionx = directionx
        self.directiony = directiony
        self.damage = damage
    def move(self, platformGroup, enemyGroup):
        self.rect.left += self.directionx * 10
        self.rect.top += self.directiony * 10
        spriteGroup = spritecollide(self, platformGroup, False)
        if pygame.sprite.spritecollideany(self, platformGroup) and spriteGroup[0].walkthrough == False:
            self.remove(self.groups())
        if pygame.sprite.spritecollideany(self, enemyGroup):
            spriteGroup = spritecollide(self, enemyGroup, False)
            for x in range(len(spriteGroup)):
                spriteGroup[x].health -= self.damage

                if spriteGroup[x].health <= 0:
                    spriteGroup[x].kill()
            self.remove(self.groups())
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
            self.left1 = int(DISPLAYSURF.get_width() / 2) - (17 * 1.4)
            self.left2 = int(DISPLAYSURF.get_width() / 2) - (36 * 1.45)
        self.height = int(DISPLAYSURF.get_height() / 2) + (14)
        if infoObject.current_h != 720:
            self.height = int(DISPLAYSURF.get_height() / 2) + (14 * 1.4)
        self.rect.update(self.left1, self.height, self.rect.width, self.rect.height)
        self.canAttack = True
    def attack(self, bulletGroup, DISPLAYSURF):
        if self.canAttack == True:
            if self.rect.left == self.left1:
                spawnLeft = self.rect.left + 30
                spawnTop = int(DISPLAYSURF.get_height() / 2) + (14)
            elif self.rect.left == self.left2:
                spawnLeft = self.rect.left + 15
                spawnTop = int(DISPLAYSURF.get_height() / 2) + (14)
            elif self.rect.left == self.left3:
                spawnLeft = self.rect.left
                if self.yDirection > 0:
                    spawnTop = int(DISPLAYSURF.get_height() / 2) + (25)
                elif self.yDirection < 0:
                    spawnTop = int(DISPLAYSURF.get_height() / 2)
                    print("in loop")
            elif self.rect.left == self.left4:
                spawnLeft = self.rect.left + 6
                if self.yDirection > 0:
                    spawnTop = int(DISPLAYSURF.get_height() / 2) + (25)
                elif self.yDirection < 0:
                    print("in loop")
                    spawnTop = int(DISPLAYSURF.get_height() / 2)
            bulletGroup.add(Bullet(DISPLAYSURF, pygame.image.load("Images/Bullet.png"), spawnLeft, spawnTop, self.xDirection, self.yDirection, self.gunDamage))
            self.canAttack = False