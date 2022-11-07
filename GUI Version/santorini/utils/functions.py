"""
Contains utility functions used throughout the project
"""

from .constants import SQUARE_SIZE, BLUE, ROWS, COLS
from .assets import MENU_BACKGROUND, CLOUD, TITLE_FONT, GRASS


def calc_pos(col, row, offset):
    """
    Given a column and row of the board and an offset calculate the correct x and y coordinates of an asset to display
    on the board
    :param col: board column
    :param row: board row
    :param offset: amount to reposition from center by
    :return: x and y coordinate of column and row
    """
    x = SQUARE_SIZE * col + SQUARE_SIZE // 2 - offset
    y = SQUARE_SIZE * row + SQUARE_SIZE // 2 - offset

    return x, y


def get_row_col_from_mouse(pos):
    """
    Given a position from a mouse click return the relevant row and column
    :param pos: position of mouse click
    :return: board row and column
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def page_template(win, title_text):
    """
    Produce basic page details including a background, title and title highlight
    :param win: pygame window to blit on
    :param title_text: text to display as title
    """
    win.blit(MENU_BACKGROUND, (0, 0))
    text = TITLE_FONT.render(title_text, True, BLUE)
    text_rect = text.get_rect()
    text_rect.center = (300, 110)

    win.blit(CLOUD, (130, 50))
    win.blit(text, text_rect)


def draw_grass(win):
    """
    Draw tiles instead of squares for game board
    :param win: pygame window
    """
    for row in range(ROWS):
        for col in range(COLS):
            x, y = calc_pos(col, row, 60)
            win.blit(GRASS, (x, y))
