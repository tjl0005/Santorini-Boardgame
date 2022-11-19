"""
Contains utility functions used throughout the project
"""
import textwrap

from .constants import SQUARE_SIZE, BLUE, PLAYER_ONE, DESC_LIMIT, WHITE
from .assets import MENU_BACKGROUND, GAME_BACKGROUND, CLOUD, TITLE_FONT, DESCRIPTION_FONT


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


def draw_grass_background(win):
    """
    Draw the background for the game as a singular image, instead of tiles
    :param win:
    """
    win.blit(GAME_BACKGROUND, (0, 0))


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
    # Title text
    text = TITLE_FONT.render(title_text, True, BLUE)
    text_rect = text.get_rect()
    text_rect.center = (300, 110)
    # Title background image
    win.blit(CLOUD, (130, 50))
    win.blit(text, text_rect)


def add_god_description(win, player, god):
    """
    Given a gods menu screen produce the correct description for the relevant player and god
    :param win: pygame window to blit on
    :param player: relevant player to display text for
    :param god: players currently selected god
    """
    # Player label and god description location depends on the player
    if player == PLAYER_ONE:
        player_loc = [150, 250]
        desc_loc = [150, 350]
    else:
        player_loc = [450, 250]
        desc_loc = [450, 350]

    # Add player label
    player_text = DESCRIPTION_FONT.render("player " + player, True, WHITE)
    player_rect = player_text.get_rect()
    player_rect.center = player_loc
    win.blit(player_text, player_rect)
    # Add god description
    desc = get_description(god)
    desc_text = textwrap.wrap(desc, DESC_LIMIT)
    write_text(desc_text, desc_loc, win)


def add_mode_description(win, mode):
    """
    When changing modes on god screen, this function will write the text describing the function
    :param win: pygame window
    :param mode: god mod (None, Simple Gods, Custom)
    """
    desc = get_description(mode)
    desc_text = textwrap.wrap(desc, DESC_LIMIT)
    desc_loc = [300, 300]  # Center of screen relative to buttons/title

    write_text(desc_text, desc_loc, win)


def write_text(description, loc, win):
    """
    Given wrapped text, write each line and maintain centrality
    :param description: text to write
    :param loc: position for text to appear
    :param win: pygame window
    """
    if len(description) > 1:
        for line in description:
            text = DESCRIPTION_FONT.render(line, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = loc
            win.blit(text, text_rect)

            loc[1] += 20


def get_description(god):
    """
    Generate the description for a given god
    :param god: used to get the relevant description
    :return: description as a string
    """
    match god:
        case "Prometheus":
            return "Your can keep building until you move a worker"
        case "Hephaestus":
            return "You can build an extra level on any building in your workers reach, excluding domes"
        case "Demeter":
            return "You can build a brand new building anywhere in your workers reach"
        case "Hermes":
            return "You have unlimited movement until you climb a building"
        case "None":
            return "No special abilities will be implemented in your game"
        case "Custom":
            return "You have full control over your move and end it when you want, bots do not work here :)"
        case _:
            return "Something broke here :)"


def god_conditions(last_move, god):
    """
    Depending upon a players last move their god will have different restrictions
    :param last_move: players last action
    :param god: players current god
    :return: string containing new conditions for the player
    """
    match last_move:
        case "building":
            match god:
                case "Prometheus":
                    return "move"
                case "Hephaestus":
                    return "upto l2"
                case "Demeter":
                    return "new"
        case "moving":
            if god == "Prometheus":
                return "build"
