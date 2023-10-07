import pygame
from editor import Editor
from game import Game
from platformer_editor.util.button import Button
from util.constants import *

# pygame variables
pygame.init()


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load(TITLE)
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.play = Button(WIDTH / 4 - 100, HEIGHT * 0.80, pygame.image.load("assets/buttons/play.png"), 1)
        self.edit = Button(2 * WIDTH / 4 - 100, HEIGHT * 0.80, pygame.image.load("assets/buttons/edit.png"), 1)
        self.settings = Button(3 * WIDTH / 4 - 100, HEIGHT * 0.80, pygame.image.load("assets/buttons/settings.png"), 1)
        self.mode = 0

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.draw()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Buttons
        if self.play.draw(self.screen):
            self.mode = 1
        elif self.edit.draw(self.screen):
            self.mode = 2
            pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
        elif self.settings.draw(self.screen):
            self.mode = 3

        pygame.display.flip()


if __name__ == "__main__":
    main = Main()
    editor = Editor()
    game = Game()

    while True:
        if main.mode == 0:
            main.play_step()
        elif main.mode == 1:
            main.mode = game.play_step()
        elif main.mode == 2:
            main.mode = editor.play_step()
