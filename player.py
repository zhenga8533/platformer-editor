import pygame
from pygame.locals import *
from util.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # player variables
        self.x = 0
        self.y = 500
        self.running = False

        # sprite variables
        super().__init__()
        self.sprites = {}
        for player_sprite in PLAYER_SPRITES:
            sprite = pygame.image.load(f'assets/player/{player_sprite}.png')
            sprite = pygame.transform.scale(sprite, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
            self.sprites[player_sprite] = sprite
        self.frame = "idle"
        self.run = 1
        self.image = None
        self.rect = None
        self.update_image()

    def update(self, keys):
        # running keys + animation
        if keys[K_d]:
            self.x += SPEED
            self.running = True
        elif keys[K_a]:
            self.x -= SPEED
            self.running = True
        else:
            self.running = False

        if self.running:
            self.run = (self.run + SPEED/20) % 3
            self.frame = f'run{int(self.run)}'
        else:
            self.frame = "idle"

        self.update_image()

    def update_image(self):
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
