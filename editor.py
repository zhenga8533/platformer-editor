import pygame
from pygame import key
from pygame.locals import *
from button import Button
from util.constants import *


class Editor:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
        pygame.display.set_caption('Stage Editor')

        self.level = 0
        self.background = pygame.image.load(BACKGROUND[self.level])
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.choice = 0

        test = pygame.image.load("assets/test.png")
        test = pygame.transform.scale(test, (TILE_SIZE * 2, TILE_SIZE * 2))
        self.buttons = []

        for row in range(5):
            for col in range(3):
                tile_button = Button(WIDTH + 128*col + 32, 128*row + 32, test, 1)
                self.buttons.append(tile_button)

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == K_UP:
                self.level = (self.level + 1) % 43
                self.background = pygame.image.load(BACKGROUND[self.level]).convert_alpha()
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Player control
        keys = key.get_pressed()
        if keys[K_q]:
            pygame.quit()
            quit()

        self.draw()
        self.clock.tick(FPS)

    def draw(self):
        self.draw_background()
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
