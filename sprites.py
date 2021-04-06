import pygame, sys

pygame.init()
import pygame
import os


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
        self.images.append(pygame.image.load(os.path.join("Images", "Player.png")))

        self.x_velocity = 0
        self.y_velocity = 0
        self.jump_height = -15

        super().__init__(self.images, 0, 0, 10, 0, 1, 0)

        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)

    def update(self):
        self.x_velocity = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_velocity = 5
        if keys[pygame.K_a]:
            self.x_velocity = -5

        #self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity


    def getShift(self):
        return self.x_velocity, self.y_velocity

    def jump(self):
        self.y_velocity = self.jump_height


##############
# Block Classes
##############

# Main Block Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, posX, posY, breakable, damage):

        super().__init__()
        self.image = image

        # position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.center = (self.posX, self.posY)

        # Object information
        self.breakable = breakable  # If True, destroy block in response to any damage
        self.damage = damage  # For Blocks such as spikes and lava, amount of damage inflicted to the player

    def update(self, shiftX, shiftY):
        self.posX -= shiftX
        self.posY -= shiftY

        self.rect.center = (self.posX, self.posY)


#Lower Block Classes
class BasicBlock(Platform):

    def __init__(self, posX, posY):

        #Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0)


class BreakableBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, True, 0)

class SpikesBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 5)

class LavaBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 5)

class DoorBlock(Platform):

    def __init__(self, posX, posY):

        # Load Images
        self.sprite = pygame.image.load('Images/Lava.png')

        super().__init__(self.sprite, posX, posY, False, 0)



class Collectables(pygame.sprite.Sprite):
    def __init__(self, string, xpos, ypos, image):
        super().__init__()
        self.name = string
        self.xpos = xpos
        self.ypos = ypos
        self.rect.update(xpos, ypos, 100, 100)
        self.image = pygame.image.load(image)

    def is_collided_with(self, char):
        if self.rect.colliderect(char.rect):
            self.kill()

    def getname(self):
        return self.name

    def updatepos(self, x, y):
        self.posx = x
        self.posy = y

    def getposx(self):
        return self.posx

    def getposy(self):
        return self.posy
