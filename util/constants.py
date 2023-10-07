import pygame
pygame.mixer.init()

# pygame constants
WIDTH = 960
HEIGHT = 640
SIDEBAR_WIDTH = 384
FPS = 60

# game constants
TITLE = "assets/background/0.png"
BACKGROUNDS = [f'assets/background/{i}.png' for i in range(1, 44)]
TILES = [f'assets/tiles/{i}.png' for i in range(15)]
TILE_SIZE = 16
ROWS = HEIGHT // TILE_SIZE
COLUMNS = WIDTH // TILE_SIZE

# Sounds
bump = pygame.mixer.Sound("assets/sounds/bump.mp3")
fall = pygame.mixer.Sound("assets/sounds/fall.mp3")
jump = pygame.mixer.Sound("assets/sounds/jump.mp3")
land = pygame.mixer.Sound("assets/sounds/land.mp3")

# player constants
PLAYER_SPRITES = ["fall", "fallen", "idle", "jump", "oof", "run0", "run1", "run2", "squat"]
PLAYER_SIZE = (TILE_SIZE * 4, TILE_SIZE * 4.5)
SPEED = 3
GRAVITY = -0.281
TERMINAL_VELOCITY = -14

# colors rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
