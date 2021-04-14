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
                self.sprites[x] = pygame.transform.scale(self.sprites[x], (int(self.sprites[x].get_width() * 0.6667), int(self.sprites[x].get_height() * 0.6667)))
            for x in range(len(self.sprites1)):
                self.sprites1[x] = pygame.transform.scale(self.sprites1[x], (int(self.sprites1[x].get_width() * 0.6667), int(self.sprites1[x].get_height() * 0.6667)))

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
        

    def update(self, direction, sword):
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
        if direction != self.currentDirection:
          self.currentDirection = direction
          if direction == -1:
              if sword.rect.left != sword.left2:
                  sword.image = pygame.transform.flip(sword.originalImage, True, False)
                  sword.rect.left = sword.left2
                  sword.xDirection = -2
                  sword.attacking = False
          else:
              if sword.rect.left != sword.left1:
                  sword.image = sword.originalImage
                  sword.rect.left = sword.left1
                  sword.xDirection = 2
                  sword.attacking = False



        

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
        self.can_double_jump = False
        super().__init__(self.images, 0, 0, 10, 0, 1, 0, 0.25)
        self.health=100
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)
        self.maxhealth=100
        self.direction = 1
        self.jumped = False
        
    def addmaxhealth(self):
        self.maxhealth+=10
  
    def update(self, sword):
        if infoObject.current_h == 720:
            self.x_velocity = int(self.x_velocity * 0.667)

        if self.x_velocity == 0 or self.y_velocity != 0:
            self.isMoving = False

        super().update(self.direction, sword)


    def addhealth(self):
        if self.health<self.maxhealth:
            self.health+=10
    def losehealth(self):
        if self.health>0:
            self.health-=10
    def doubleJump(self):
        self.can_double_jump=True
    def hasDoubleJumped(self):
        return self.jumped
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
        if infoObject.current_h == 720:
            self.y_velocity = int(self.y_velocity * 0.667)
            weapon.y_velocity = int(weapon.y_velocity * 0.667)


##############
# Enemy Classes
##############
class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprites, directionX):
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
                self.sprites[x] = pygame.transform.scale(self.sprites[x], (int(self.sprites[x].get_width() * 0.6667), int(self.sprites[x].get_height() * 0.6667)))
            for x in range(len(self.sprites1)):
                self.sprites1[x] = pygame.transform.scale(self.sprites1[x], (int(self.sprites1[x].get_width() * 0.6667), int(self.sprites1[x].get_height() * 0.6667)))
        self.image = self.sprites[self.currentSprite]
        # position values
        self.rect = self.image.get_rect()
        self.currentDirection = 1


    def update(self, direction):
        if direction != self.currentDirection:
            self.currentDirection = direction
            if direction == -1:
                self.image = self.sprites1[int(self.currentSprite)]
            else:
                self.image = self.sprites[int(self.currentSprite)]

    ##############
class BasicEnemy(Enemy):
    def __init__(self, DISPLAYSURF, posX, posY, health, damage):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load("Images/Character0.png"))
        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_height = -18
        self.health = 100
        super().__init__(self.images, 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = [posX, posY]
        self.direction = 1
        self.health = health
        self.damage = damage
##############
# Block Classes
##############

# Main Block Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, posX, posY, breakable, damage, walkthrough):

        super().__init__()
        self.image = image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6667), int(self.image.get_height() * 0.6667)))

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
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0, False)

class BreakableBlock(Platform):

    #  C

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

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

        super().__init__(self.sprite, posX, posY, False, 5, False)

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
class Sword (pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        self.originalImage = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6667), int(self.image.get_height() * 0.6667)))
            self.originalImage = pygame.transform.scale(self.originalImage, (int(self.originalImage.get_width() * 0.6667), int(self.originalImage.get_height() * 0.6667)))
        self.rect = self.image.get_rect()
        self.y_velocity = 0
        self.xDirection = 2
        self.attacking = False
        self.attackingCount = 8
        self.swordDamage = 10
        self.left1 = int(DISPLAYSURF.get_width() / 2) + 20
        self.left2 = int(DISPLAYSURF.get_width() / 2) - 36
        if infoObject.current_h != 720:
            self.left1 = int(DISPLAYSURF.get_width() / 2) + (20*1.667)
            self.left2 = int(DISPLAYSURF.get_width() / 2) - (36*1.667)
        if infoObject.current_h != 720:
            self.height =int(DISPLAYSURF.get_height()/2) + (14*1.5)
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