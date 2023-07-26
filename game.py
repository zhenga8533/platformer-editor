import pygame
from pygame import key
from pygame.locals import *
import csv
import os
from player import Player
from util.tile import Tile
from util.constants import *


class Game:
    def __init__(self):
        # pygame variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Fall Peasant')

        # load all levels
        self.world = [
            [[-1 for i in range(WIDTH // TILE_SIZE)] for j in range(HEIGHT // TILE_SIZE)]
            for k in range(len(BACKGROUNDS))
        ]
        for level in range(len(BACKGROUNDS)):
            if os.path.exists(f'data/level_{level}.csv'):
                with open(f'data/level_{level}.csv') as csvfile:
                    reader = csv.reader(csvfile)
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            self.world[level][x][y] = int(tile)
        self.level = 0
        self.background = None

        # Setup tile buttons
        self.tiles = []
        tile = 0
        for row in range(5):
            for col in range(3):
                # Load image
                image = pygame.image.load(TILES[tile])
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                self.tiles.append(image)
                tile += 1

        # load player and tiles into sprites
        self.tile_sprites = None
        self.player = Player()
        self.update_stage()

    def update_stage(self):
        self.background = pygame.image.load(BACKGROUNDS[self.level])
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.tile_sprites = pygame.sprite.Group()
        for y, row in enumerate(self.world[self.level]):
            for x, tile in enumerate(row):
                if tile != -1:
                    self.tile_sprites.add(Tile(x * TILE_SIZE, y * TILE_SIZE, self.tiles[tile]))

    def play_step(self):
        # Single click player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    quit()
            elif event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    self.player.jump()

        # Update player
        self.player.update(key.get_pressed(), self.tile_sprites)

        # Update level
        if self.player.rect.bottom < 0:
            self.level += 1
            self.player.rect.y = HEIGHT
            self.player.update_image()
            self.update_stage()
        elif self.player.rect.top > HEIGHT:
            self.level -= 1
            self.player.rect.y = 0
            self.player.update_image()
            self.update_stage()

        # Update game
        self.draw()
        self.clock.tick(FPS)

    def draw(self):
        self.draw_background()
        self.screen.blit(self.player.image, self.player.rect)
        pygame.draw.rect(self.screen, WHITE, self.player.hitbox, 1)
        self.draw_stage()
        pygame.display.flip()

    # Draws background and grid
    def draw_background(self):
        # background
        self.screen.fill(DARK_GRAY)
        self.screen.blit(self.background, (0, 0))

    # Draw tiles onto stage
    def draw_stage(self):
        self.tile_sprites.draw(self.screen)
