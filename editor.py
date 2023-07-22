import pygame
from pygame import key, mouse
from pygame.locals import *
from button import Button
from util.constants import *


class Editor:
    def __init__(self):
        # pygame variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
        pygame.display.set_caption('Stage Editor')

        # stage variables
        self.world = [
            [[-1 for i in range(WIDTH // TILE_SIZE)] for j in range(HEIGHT // TILE_SIZE)]
            for k in range(len(BACKGROUND))
        ]
        self.level = 0
        self.background = pygame.image.load(BACKGROUND[self.level])
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Setup tile buttons
        self.tiles = []
        self.buttons = []
        self.choice = 0
        tile = 0
        for row in range(5):
            for col in range(3):
                # Load image
                image = pygame.image.load(TILES[tile])
                image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                self.tiles.append(image)
                image = pygame.transform.scale(image, (TILE_SIZE * 2, TILE_SIZE * 2))
                tile += 1

                # Create button
                button = Button(WIDTH + 128*col + 32, 128*row + 32, image, 1)
                self.buttons.append(button)

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.level = (self.level + 1) % 43
                    self.background = pygame.image.load(BACKGROUND[self.level]).convert_alpha()
                    self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                elif event.key == K_DOWN:
                    self.level = self.level - 1 if self.level != 0 else 0
                    self.background = pygame.image.load(BACKGROUND[self.level]).convert_alpha()
                    self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Player mouse control
        mouses = mouse.get_pressed()
        x, y = mouse.get_pos()
        if mouses[0]:
            if x <= WIDTH and y <= HEIGHT:
                self.world[self.level][y // TILE_SIZE][x // TILE_SIZE] = self.choice
        elif mouses[2]:
            if x <= WIDTH and y <= HEIGHT:
                self.world[self.level][y // TILE_SIZE][x // TILE_SIZE] = -1
        # Player keyboard control
        keys = key.get_pressed()
        if keys[K_q]:
            pygame.quit()
            quit()

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

        # 16px16p grid
        for col in range(COLUMNS + 1):
            pygame.draw.line(self.screen, GRAY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
        for row in range(ROWS + 1):
            pygame.draw.line(self.screen, GRAY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

        # buttons grid
        for i, button in enumerate(self.buttons):
            if button.draw(self.screen):
                self.choice = i
        # selected button
        pygame.draw.rect(self.screen, WHITE, self.buttons[self.choice].rect, 3)

    # Draw tiles onto stage
    def draw_stage(self):
        for y, row in enumerate(self.world[self.level]):
            for x, tile in enumerate(row):
                if tile != -1:
                    self.screen.blit(self.tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))
