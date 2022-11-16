"""
Contains relevant classes to be used for presenting different menus/screens to the player. Contains the start and
options menu as well as the winning and worker position selection screen

When pages are initialised they must be updated for each pygame tick for proper functionality
"""
import pygame

from ..components.button import Button
from ..utils.functions import page_template
from ..utils.assets import SUPPORTER, MESSAGE_FONT
from ..utils.constants import BUTTON_SIZE_ONE, BUTTON_SIZE_TWO, WHITE


class Start:
    """
    Start screen of the game, allows the user to either start a new game, view the options menu or exit the game
    """
    def __init__(self, win):
        self.win = win
        self.start_button = Button(300, 200, "Start", BUTTON_SIZE_ONE)  # Begin new game
        self.options_button = Button(300, 250, "Options", BUTTON_SIZE_ONE)  # View options menu
        self.exit_button = Button(300, 300, "Exit", BUTTON_SIZE_ONE)  # Close application

    def update(self, event):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :return: new game state
        """
        page_template(self.win, "Santorini")  # Set background and display title

        # Ensure buttons are highlighted
        self.start_button.update()
        self.options_button.update()
        self.exit_button.update()
        # Display buttons
        self.start_button.draw(self.win)
        self.options_button.draw(self.win)
        self.exit_button.draw(self.win)
        # Handle button clicks
        start_clicked = self.start_button.handle_event(event, "display")
        options_clicked = self.options_button.handle_event(event, "display")
        self.exit_button.handle_event(event, "display")

        # If clicked handle_event returns true
        if start_clicked:
            self.start_button.hovered = False
            return "play"
        elif options_clicked:
            self.options_button.hovered = False
            return "options"

        pygame.display.update()


class Options:
    """
    Display options menu including the main menu button, player mode button (Two Player, Minimax or Greedy) and starting
     worker positions
    """
    def __init__(self, win):
        self.win = win
        self.state = "options"
        self.game_type = "Two Player"
        self.start_select = "Default Positions"
        self.return_button = Button(300, 200, "back", BUTTON_SIZE_TWO)  # Return to menu
        self.option_button = Button(300, 250, self.game_type, BUTTON_SIZE_TWO)  # Two player, Minimax or Greedy
        self.select_button = Button(300, 300, self.start_select, BUTTON_SIZE_TWO)  # User decides starting positions

    def update(self, event):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :return:
        """
        page_template(self.win, "options")
        self.return_button.draw(self.win)
        self.option_button.draw(self.win)
        self.select_button.draw(self.win)

        self.return_button.update()
        self.option_button.update()
        self.select_button.update()

        # Update state to go back to start menu
        if self.return_button.handle_event(event, "options"):
            self.state = "start"
            self.return_button.hovered = False
        # Not changing screens
        else:
            self.state = "options"

        game_type = self.option_button.handle_event(event, "options")
        selection_type = self.select_button.handle_event(event, "options")

        # Go through list of play modes
        if game_type == "Two Player":
            self.game_type = "Two Player"
        elif game_type == "Minimax":
            self.game_type = "Minimax"
        elif game_type == "Greedy":
            self.game_type = "Greedy"
        # Go through list of starting position options
        if selection_type == "Default Positions":
            self.start_select = "Default Positions"
        elif selection_type == "User Positions":
            self.start_select = "User Positions"

        self.option_button.update_text(self.game_type)
        self.select_button.update_text(self.start_select)

        pygame.display.update()


class Winner:
    """
    Page to show when the game.is_over is true to congratulate the relevant player
    """
    def __init__(self, win):
        self.winner = ""
        self.win = win
        self.state = "win_screen"
        self.return_button = Button(300, 250, "return", BUTTON_SIZE_TWO)

    def win_message(self):
        """
        Inserts message on window state congratulating relevant player
        """
        text = MESSAGE_FONT.render('Congratulations Player {}'.format(self.winner), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (300, 200)

        self.win.blit(text, text_rect)  # Show victory text
        self.win.blit(SUPPORTER, (50, 300))  # Show player supporter

    def update(self, event, winner):
        """
        Used to generate the initial menu and enable the buttons to be functional.
        :param event: pygame event, used to decide button action
        :param winner: winning player
        """
        page_template(self.win, "Winner")
        self.winner = winner
        self.win_message()

        self.return_button.draw(self.win)
        self.return_button.update()

        if self.return_button.handle_event(event, "options"):
            self.state = "start"
            self.return_button.hovered = False
        else:
            self.state = "win_screen"

        pygame.display.update()
