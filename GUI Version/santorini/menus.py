import pygame

from .components.button import Button
from .constants import button_size_one, button_size_two, background, cloud, squirk, BLUE

font = pygame.font.Font(squirk, 48)


class Start:
    def __init__(self, win):
        self.colour = (255, 255, 255)
        self.win = win
        self.start_button = Button(300, 200, "Start", button_size_one)
        self.options_button = Button(300, 250, "Options", button_size_one)
        self.exit_button = Button(300, 300, "Exit", button_size_one)

    def title(self):
        text = font.render('Santorini', True, BLUE)
        text_rect = text.get_rect()
        text_rect.center = (300, 110)

        self.win.blit(cloud, (130, 50))
        self.win.blit(text, text_rect)

    def update(self, event):
        self.win.blit(background, (0, 0))
        self.title()
        self.start_button.update()
        self.options_button.update()
        self.exit_button.update()

        self.start_button.draw(self.win)
        self.options_button.draw(self.win)
        self.exit_button.draw(self.win)

        start_clicked = self.start_button.handle_event(event, "display")
        options_clicked = self.options_button.handle_event(event, "display")
        self.exit_button.handle_event(event, "display")

        if start_clicked:
            self.start_button.hovered = False
            return "play"
        elif options_clicked:
            self.options_button.hovered = False
            return "options"

        pygame.display.update()


class Options:
    def __init__(self, win):
        self.colour = (255, 255, 255)
        self.win = win
        self.state = "options"
        self.game_type = "Two Player"
        self.start_select = "Default Positions"
        self.return_button = Button(300, 200, "back", button_size_two)
        self.option_button = Button(300, 250, self.game_type, button_size_two)
        self.select_button = Button(300, 300, self.start_select, button_size_two)

    def title(self):
        text = font.render('Options', True, BLUE)
        text_rect = text.get_rect()
        text_rect.center = (300, 110)

        self.win.blit(cloud, (130, 50))
        self.win.blit(text, text_rect)

    def update(self, event):
        self.win.blit(background, (0, 0))
        self.title()

        self.return_button.draw(self.win)
        self.option_button.draw(self.win)
        self.select_button.draw(self.win)

        self.return_button.update()
        self.option_button.update()
        self.select_button.update()

        if self.return_button.handle_event(event, "options"):
            self.state = "start"
            self.return_button.hovered = False
        else:
            self.state = "options"

        game_type = self.option_button.handle_event(event, "options")
        selection_type = self.select_button.handle_event(event, "options")

        if game_type == "Two Player":
            self.game_type = "Two Player"
        elif game_type == "Minimax":
            self.game_type = "Minimax"
        elif game_type == "Greedy":
            self.game_type = "Greedy"

        if selection_type == "Default Positions":
            self.start_select = "Default Positions"
        elif selection_type == "User Positions":
            self.start_select = "User Positions"

        self.option_button.update_text(self.game_type)
        self.select_button.update_text(self.start_select)

        pygame.display.update()
