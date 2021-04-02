import pygame
import os


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Images", "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Images", "TestPlatform.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2 + self.image.get_height())
