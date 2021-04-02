import pygame
import os


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Images", "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.x_velocity = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_velocity = 5
        if keys[pygame.K_a]:
            self.x_velocity = -5
        self.rect.x += self.x_velocity


class Platform(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Images", "TestPlatform.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2 + self.image.get_height())
