"""
Constants used throughout the project
"""
# Board variables
FPS = 60
ROWS, COLS = 5, 5
HEIGHT, WIDTH = 600, 600
SQUARE_SIZE = WIDTH // COLS

# Sizes for any buttons
BUTTON_SIZE_ONE = (100, 40)
BUTTON_SIZE_TWO = (200, 40)

# Starting positions for workers
DEFAULT_POSITIONS = [(1, 2), (2, 1), (2, 3), (3, 2)]
ALL_POSITIONS = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                 (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                 (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                 (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                 ]

# Board/Piece colours
WHITE = (255, 255, 255)
BLUE = (21, 176, 231)
LIGHT_GREEN = (160, 164, 103)
GREEN = (100, 164, 103)
DARK_GREEN = (117, 143, 78)

# Player References
PLAYER_ONE = "One"
PLAYER_TWO = "Two"
PLAYER_THREE = "Three"
PLAYER_FOUR = "Four"
