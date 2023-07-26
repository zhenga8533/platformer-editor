import pygame
from pygame.locals import *
from util.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # player variables
        self.velocity = [0.0, 0.0]
        self.jump_charge = 0
        self.jump_direction = 0

        # load sprites
        self.sprites = {}
        for player_sprite in PLAYER_SPRITES:
            sprite = pygame.image.load(f'assets/player/{player_sprite}.png').convert_alpha()
            sprite = pygame.transform.scale(sprite, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
            self.sprites[player_sprite] = sprite
        # frame control
        self.frame = "idle"
        self.direction = False
        self.run = 0
        self.running = False
        self.jumping = False
        self.jumped = False

        # sprite variables
        super().__init__()
        self.image = None
        self.rect = self.sprites["idle"].get_rect(bottomleft=(375, 375))
        self.update_image()

    def jump(self):
        self.jump_charge = min(self.jump_charge, -2 * TERMINAL_VELOCITY)
        self.velocity[0] = self.jump_direction * self.jump_charge / 3
        self.velocity[1] = self.jump_charge
        self.jump_charge = 0
        self.jumped = True
        self.jumping = False

    def update(self, keys, sprites):
        # y motion
        self.velocity[1] = max(self.velocity[1] + GRAVITY, TERMINAL_VELOCITY)
        self.rect.y -= self.velocity[1]
        # y collision
        collided = pygame.sprite.spritecollideany(self, sprites)
        if collided:
            if self.velocity[1] < 0:
                self.rect.bottom = collided.rect.top
                self.velocity[1] = GRAVITY
                self.velocity[0] = 0
                self.jumped = False
                self.jump_direction = 0
            else:
                self.rect.top = collided.rect.bottom
                self.velocity[1] = GRAVITY

        # x motion
        self.rect.x += self.velocity[0]

        # player control keys
        if keys[K_SPACE]:
            self.jump_charge += 1
            self.jumping = True

        if not self.jumped:
            if keys[K_d]:
                self.direction = True
                if not self.jumping:
                    self.rect.x += SPEED
                    self.running = True
                    self.jump_direction = 0
                else:
                    self.jump_direction = 1
            elif keys[K_a]:
                self.direction = False
                if not self.jumping:
                    self.rect.x -= SPEED
                    self.running = True
                    self.jump_direction = 0
                else:
                    self.jump_direction = -1
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
