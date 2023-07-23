# pygame constants
WIDTH = 960
HEIGHT = 640
SIDEBAR_WIDTH = 384
FPS = 60

# game constants
BACKGROUNDS = [f'assets/background/{i}.png' for i in range(1, 44)]
TILES = [f'assets/tiles/{i}.png' for i in range(15)]
TILE_SIZE = 32
ROWS = HEIGHT // TILE_SIZE
COLUMNS = WIDTH // TILE_SIZE

# colors rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
