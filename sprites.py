import pygame

##################
#Character Classes
##################

#Main Character Class
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

        #position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.topleft = [posX, posY]

        # Basic direction values for the character so that Andy can work on the weapons
        # These can be used as multipliers for speed when the character and other objects are moving
        self.directionX = directionX  # Can either be -1 or 1 (Left or Right)
        self.directionY = directionY  # Can either be -1, 0, or 1 (Down, Neutral, Up)


#Lower Character Classes
class MainCharacter(Character):

    #Basic initialization class that supports different directions for the sprite
    def __init__(self, sprites, posX, posY, directionX, directionY):

        super().__init__()




##############
#Block Classes
##############

#Main Block Class
class Platform(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, breakable, damage):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        #position values
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.topleft = [posX, posY]

        #Object information
        self.breakable = breakable           #If True, destroy block in response to any damage
        self.damage = damage                 #For Blocks such as spikes and lava, amount of damage inflicted to the player


#Lower Block Classes
class BasicBlock(Platform):

    def __init__(self, sprites, posX, posY):

        #Load Images

        super.__init__(sprites, posX, posY, False, 0)


class BreakableBlock(Platform):

    def __init__(self, sprites, posX, posY):

        # Load Images

        super.__init__(sprites, posX, posY, True, 0)

class SpikesBlock(Platform):

    def __init__(self, sprites, posX, posY):

        # Load Images

        super.__init__(sprites, posX, posY, False, 5)

class LavaBlock(Platform):

    def __init__(self, sprites, posX, posY):

        # Load Images
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Lava.png'))

        super.__init__(sprites, posX, posY, False, 5)