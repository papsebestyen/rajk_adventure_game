import pandas as pd

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
TEXTBOX_COLOR = (255, 243, 230)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60 # loop/s
SPEED = 5 # tile/s

MOVE_FPS = 5

# Question settings
TEXTSIZE = 20
GAMETIME = 5 # Game time in minute


TITLE = "Rajk Adventure Game"

TILESIZE = 32

STAR_IMG = 'star.png'
STAR_EMPTY_IMG = 'star_empty.png'

PLAYER_IMG = 'Alex'

CHAR_DIRS = ('right_0', 'up_0', 'left_0', 'down_0', 'right_1', 'right_2', 'up_1', 'up_2', 'left_1', 'left_2', 'down_1', 'down_2')
    
MOBS = pd.read_csv('mob_settings.csv', sep = ';', encoding = 'latin2', index_col = 0).assign(correct = None).to_dict(orient = 'index')

YEARS = {
    0: 'UF',
    1: 'POSZT UF',
    2: 'HARMAD',
    3: 'NEGYED',
    4: 'ÖTÖD'
}

MONTHS = {
    0: 'JÚLIUS',
    1: 'AUGUSZTUS',
    2: 'SZEPTEMBER',
    3: 'OKTÓBER',
    4: 'NOVEMBER',
    5: 'DECEMBER',
    6: 'JANUÁR',
    7: 'FEBRUÁR',
    8: 'MÁRCIUS',
    9: 'ÁPRILIS',
    10: 'MÁJUS',
    11: 'JÚNIUS'
}