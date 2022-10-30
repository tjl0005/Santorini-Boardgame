import pygame

from .button import Button
from .constants import button_size_one, button_size_two


class Start:
    def __init__(self, win):
        self.colour = (255, 255, 255)
        self.win = win
        self.start_button = Button(300, 200, "Start", button_size_one)
        self.options_button = Button(300, 250, "Options", button_size_one)
        self.exit_button = Button(300, 300, "Exit", button_size_one)

    def title(self):
        self.win.fill(self.colour)
        font = pygame.font.SysFont("calibre", 60)
        text = font.render('Santorini', True, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (300, 100)

        self.win.blit(text, text_rect)

    def buttons(self):
        pos = pygame.mouse.get_pos()
        self.start_button.update(self.win)
        self.start_button.change_colour(pos)
        self.options_button.update(self.win)
        self.options_button.change_colour(pos)
        self.exit_button.update(self.win)
        self.exit_button.change_colour(pos)

    def get_state(self, state, pos):
        state = self.start_button.check_display(pos, state)
        state = self.options_button.check_display(pos, state)
        state = self.exit_button.check_display(pos, state)

        return state

    # noinspection DuplicatedCode
    def update(self, pos):
        self.title()
        self.buttons()

        self.start_button.update(self.win)
        self.start_button.change_colour(pos)
        self.options_button.update(self.win)
        self.options_button.change_colour(pos)
        self.exit_button.update(self.win)
        self.exit_button.change_colour(pos)

        pygame.display.update()


# noinspection DuplicatedCode
class Options:
    def __init__(self, win):
        self.colour = (255, 255, 255)
        self.win = win
        self.state = "options"
        self.game_type = "two"
        self.positions = "Default Positions"
        self.return_button = Button(300, 200, "Back to start", button_size_two)
        self.option_button = Button(300, 250, self.game_type, button_size_two)
        self.position_button = Button(300, 300, self.positions, button_size_two)

    def title(self):
        self.win.fill(self.colour)
        font = pygame.font.SysFont("calibre", 60)
        text = font.render('Option Menu', True, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (300, 100)

        self.win.blit(text, text_rect)

    def buttons(self, pos):
        self.return_button.change_colour(pos)
        self.option_button.update(self.win)
        self.option_button.change_colour(pos)
        self.position_button.update(self.win)
        self.position_button.change_colour(pos)

    def update(self, pos):
        self.title()

        self.return_button.update(self.win)
        self.return_button.change_colour(pos)
        self.option_button.update(self.win)
        self.option_button.change_colour(pos)
        self.position_button.update(self.win)
        self.position_button.change_colour(pos)
        pygame.display.update()

    def get_updates(self, pos):
        start_state = self.return_button.check_options(pos, "start")
        game_type = self.option_button.check_options(pos, self.game_type)

        if start_state:
            self.state = "start"
        elif not start_state:
            self.state = "options"

        if game_type == "two":
            self.game_type = "two"
        elif game_type == "minimax":
            self.game_type = "minimax"

        self.option_button = Button(300, 250, self.game_type, button_size_two)
