import pygame, sys

pygame.init()
import pygame
import os

infoObject = pygame.display.Info()

##################
# Character Classes
##################

# Main Character Class
class Character(pygame.sprite.Sprite):
    def __init__(self, sprites, posX, posY, health, damage, directionX, directionY):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6667), int(self.image.get_height() * 0.6667)))
        if directionX != 0:
            # For when the sprite is reversed
            self.sprites1 = []
            for i in range(len(self.sprites)):
                self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))

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

        
class MainCharacter(Character):
    def __init__(self, DISPLAYSURF):
        #Pass sprites as arrays to allow for easier animations
        self.images = []
        self.images.append(pygame.image.load(os.path.join("Images", "Player2.png")))
        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_height = -18
        self.can_double_jump=False
        super().__init__(self.images, 0, 0, 10, 0, 1, 0)
        self.health=100
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)

    def update(self):

        self.x_velocity = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_velocity = 5
        if keys[pygame.K_a]:
            self.x_velocity = -5
        if infoObject.current_h == 720:
            self.x_velocity = int(self.x_velocity * 0.667)

    def addhealth(self):
        if self.health<100:
            self.health+=10
    def losehealth(self):
        if self.health>0:
            self.health-=10
    def doubleJump(self):
        self.can_double_jump=True
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
        print(self.y_velocity)
        return self.x_velocity, self.y_velocity

    def jump(self, weapon):
        self.y_velocity = self.jump_height
        weapon.y_velocity = self.jump_height
        if infoObject.current_h == 720:
            self.y_velocity = int(self.y_velocity * 0.667)
            weapon.y_velocity = int(weapon.y_velocity * 0.667)


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

    def update(self, shiftX, shiftY):
        self.posX -= shiftX
        self.posY -= shiftY

        self.rect.center = (self.posX, self.posY)


#Lower Block Classes
class BasicBlock(Platform):

    def __init__(self, posX, posY):

        #Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0, False)


class BreakableBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, True, 0, False)

class SpikesBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 5, True)

class LavaBlock(Platform):

    #  L

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 5, True)

class DoorBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0, False)



class Collectables(Platform):
    def __init__(self, name, xpos, ypos, image):

        self.name = name

        super().__init__(image, xpos, ypos, False, 0, True)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()
            if self.name=="health":
                char.addhealth()
            elif self.name=="doublejump":
                char.doubleJump()

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

class AddHealth(Collectables):

    # A

    def __init__(self, xpos, ypos):

        image = pygame.image.load('Images/Health.png')

        super().__init__("health", xpos, ypos, image)

##############
#Weapons
##############
class Sword (pygame.sprite.Sprite):
    def __init__(self, _left, _top, _image):
        pygame.sprite.Sprite.__init__(self)
        self.image = _image
        if infoObject.current_h == 720:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6667), int(self.image.get_height() * 0.6667)))
        self.rect = self.image.get_rect()
        self.rect.update(_left, _top, self.rect.width, self.rect.height)
        self.x_velocity = 0
        self.y_velocity = 0
        self.xMove = 0
        self.yMove = 0
        self.xDirection = 2
        self.yDirection = 0
        self.attacking = False
        self.attackingCount = 8
    def update(self):
        self.x_velocity = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_velocity = 5
        if keys[pygame.K_a]:
            self.x_velocity = -5

        self.attack()
    def attack(self):
        if self.attacking == True:
            self.rect.x += self.xDirection
            self.rect.y += self.yDirection
            self.attackingCount -= 1
            if self.attackingCount == 0:
                self.attacking = False
                self.attackingCount = 8
                self.xDirection = 2
            elif self.attackingCount <= 4:
                self.xDirection = -2
