import pygame
from editor import Editor
from game import Game

# pygame variables
pygame.init()


if __name__ == "__main__":
    game = Game()

    while True:
        game.play_step()