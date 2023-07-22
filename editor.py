import pygame
from pygame.locals import *
from util.constants import *


class Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Stage Editor')

        self.level = 0
        self.background = pygame.image.load(BACKGROUND[self.level]).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.draw()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
