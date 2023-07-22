import pygame
from editor import Editor

# pygame variables
pygame.init()


if __name__ == "__main__":
    editor = Editor()

    while True:
        editor.play_step()