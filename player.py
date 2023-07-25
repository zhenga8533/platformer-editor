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
        self.jump_charge = 0

        # load sprites
        self.sprites = {}
        for player_sprite in PLAYER_SPRITES:
            sprite = pygame.image.load(f'assets/player/{player_sprite}.png')
            sprite = pygame.transform.scale(sprite, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
            self.sprites[player_sprite] = sprite
        # frame control
        self.frame = "idle"
        self.direction = True
        self.run = 0
        self.running = False
        self.jumping = False
        self.jumped = False

        # sprite variables
        super().__init__()
        self.image = None
        self.rect = None
        self.update_image()

    def jump(self):
        self.y_velocity = min(self.jump_charge, 20)
        self.jump_charge = 0
        self.jumped = True
        self.jumping = False

    def update(self, keys, sprites):
        # gravity
        self.y_velocity = max(self.y_velocity + GRAVITY, TERMINAL_VELOCITY)
        self.y -= self.y_velocity
        # y collision
        collided = pygame.sprite.spritecollideany(self, sprites)
        if collided and self.y_velocity < 0:
            self.y = collided.y
            self.y_velocity = GRAVITY
            self.jumped = False

        # player control keys
        if keys[K_SPACE]:
            self.jump_charge += 1
            self.jumping = True

        if not self.jumped:
            if keys[K_d]:
                self.x += SPEED
                self.running = True
                self.direction = True
            elif keys[K_a]:
                self.x -= SPEED
                self.running = True
                self.direction = False
            else:
                self.running = False

        # Control sprite frame
        if self.jumped:
            self.frame = "jump"
        elif self.jumping:
            self.frame = 'squat'
        elif self.running:
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
