import pygame
from pygame import key
from pygame.locals import *
import csv
import os
from util.constants import *


class Game:
    def __init__(self):
        # pygame variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Stage Editor')

        # load levels
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
        self.background = pygame.image.load(BACKGROUNDS[self.level])
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

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

        # Player keyboard control
        keys = key.get_pressed()
        if keys[K_SPACE]:
            pass

        # Update game
        self.draw()
        self.clock.tick(FPS)

    def draw(self):
        self.draw_background()
        self.draw_stage()
        pygame.display.flip()

    # Draws background and grid
    def draw_background(self):
        # background
        self.screen.fill(DARK_GRAY)
        self.screen.blit(self.background, (0, 0))

    # Draw tiles onto stage
    def draw_stage(self):
        for y, row in enumerate(self.world[self.level]):
            for x, tile in enumerate(row):
                if tile != -1:
                    self.screen.blit(self.tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))
