import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Obstacle variables
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
