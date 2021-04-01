import pygame


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2 + self.image.get_height())