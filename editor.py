from pygame import key, mouse
from pygame.locals import *
import csv
import os
from platformer_editor.util.button import Button
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
            for k in range(len(BACKGROUNDS))
        ]
        self.level = 0
        self.background = pygame.image.load(BACKGROUNDS[self.level])
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
                image = pygame.transform.scale(image, (TILE_SIZE * 4, TILE_SIZE * 4))
                self.tiles.append(pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE)))
                tile += 1

                # Create button
                button = Button(WIDTH + 128*col + 32, 112*row + 32, image, 1)
                self.buttons.append(button)

        self.load_button = Button(WIDTH + 32, 592, pygame.image.load("assets/buttons/load.png"), 0.8)
        self.reset_button = Button(WIDTH + 160, 592, pygame.image.load("assets/buttons/reset.png"), 0.8)
        self.save_button = Button(WIDTH + 288, 592, pygame.image.load("assets/buttons/save.png"), 0.8)

    def play_step(self):
        # Single click player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.level = (self.level + 1) % len(BACKGROUNDS)
                    self.background = pygame.image.load(BACKGROUNDS[self.level]).convert_alpha()
                    self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                elif event.key == K_DOWN:
                    self.level = self.level - 1 if self.level != 0 else len(BACKGROUNDS) - 1
                    self.background = pygame.image.load(BACKGROUNDS[self.level]).convert_alpha()
                    self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
                elif event.key == K_ESCAPE:
                    pygame.display.set_mode((WIDTH, HEIGHT))
                    return 0

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
        return 2

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

        # tiles grid
        for i, button in enumerate(self.buttons):
            if button.draw(self.screen):
                self.choice = i
        # selected tile
        pygame.draw.rect(self.screen, WHITE, self.buttons[self.choice].rect, 3)

        # state buttons
        if self.load_button.draw(self.screen):  # load level data from csv file
            if not os.path.exists(f'data/level_{self.level}.csv'):
                print("There is no save data!")
            else:
                with open(f'data/level_{self.level}.csv') as csvfile:
                    reader = csv.reader(csvfile)
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            self.world[self.level][x][y] = int(tile)

        if self.reset_button.draw(self.screen):  # clears current level to base state
            self.world[self.level] = [[-1 for i in range(WIDTH // TILE_SIZE)] for j in range(HEIGHT // TILE_SIZE)]

        if self.save_button.draw(self.screen):  # save level data tp csv file
            with open(f'data/level_{self.level}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in self.world[self.level]:
                    writer.writerow(row)

    # Draw tiles onto stage
    def draw_stage(self):
        for y, row in enumerate(self.world[self.level]):
            for x, tile in enumerate(row):
                if tile != -1:
                    self.screen.blit(self.tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))
