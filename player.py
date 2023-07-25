import pygame
from pygame.locals import *
from util.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # player variables
        self.x = 0
        self.x_velocity = 0
        self.y = 550
        self.y_velocity = GRAVITY
        self.running = False

        # sprite variables
        super().__init__()
        self.sprites = {}
        for player_sprite in PLAYER_SPRITES:
            sprite = pygame.image.load(f'assets/player/{player_sprite}.png')
            sprite = pygame.transform.scale(sprite, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
            self.sprites[player_sprite] = sprite
        self.frame = "idle"
        self.run = 0
        self.direction = True
        self.image = None
        self.rect = None
        self.update_image()

    def update(self, keys, sprites):
        # gravity
        self.y_velocity = max(self.y_velocity + GRAVITY, TERMINAL_VELOCITY)
        self.y -= self.y_velocity

        # y collision
        collided = pygame.sprite.spritecollideany(self, sprites)
        if collided:
            self.y = collided.y
            self.y_velocity = GRAVITY

        # keys + animation
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    self.y_velocity = self.charge

        if keys[K_SPACE]:
            self.y_velocity = 15
        elif keys[K_d]:
            self.x += SPEED
            self.running = True
            self.direction = True
        elif keys[K_a]:
            self.x -= SPEED
            self.running = True
            self.direction = False
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
        if not self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [self.x, self.y]
