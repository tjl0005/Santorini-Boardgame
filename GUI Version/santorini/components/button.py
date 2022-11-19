"""
Contains the button class used to create button objects with functionality
"""
import pygame

from ..utils.assets import BUTTON_ICON, BUTTON_FONT

pygame.init()


class Button:
    """
    Class used to generate functional buttons
    """
    def __init__(self, x_pos, y_pos, text_input, button_size):
        self.image = pygame.transform.scale(BUTTON_ICON, button_size)  # Button graphic
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = BUTTON_FONT.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.hovered = False  # User mouse on button

    def update_colour(self):
        """
        Detect if user hovering over button and change text colour to reflect this
        """
        if self.hovered:
            self.text = BUTTON_FONT.render(self.text_input, True, "lightblue")
        else:
            self.text = BUTTON_FONT.render(self.text_input, True, "white")

    def draw(self, win):
        """
        Draw button text and image on the board
        :param win: pygame window
        """
        win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    def update_text(self, text):
        """
        Update the button text
        :param text: new button text
        """
        self.text_input = text
        self.text = BUTTON_FONT.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.update_colour()

    def handle_event(self, event, button_type):
        """
        Detect if button is being hovered over and also detect if a button is pressed. If a button is pressed perform
        given action
        :param event: pygame event
        :param button_type: origin of button e.g. option menu
        :return: True if just detecting button press
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                if button_type in ["confirm", "cancel", ]:
                    return True
                match button_type:
                    case "mode":
                        return self.handle_mode_event()
                    case "display":
                        return self.handle_display_event()
                    case "options":
                        return self.handle_options_event()
                    case "gods":
                        return self.handle_gods_event()
                    case "god_mode":
                        return self.handle_god_mode_event()

    def handle_mode_event(self):
        """
        :return: updated mode
        """
        if self.text_input == "moving":
            return "building"
        elif self.text_input == "building":
            return "moving"
        else:
            return "start"

    def handle_display_event(self):
        """
        :return: updated state
        """
        if self.text_input == "Exit":
            exit()
        else:
            return True

    def handle_options_event(self):
        """
        :return: the updated option
        """
        if self.text_input in ["back", "return", "confirm positions", "player one", "player two"]:
            return True
        elif self.text_input == "Minimax":
            return "Greedy"
        elif self.text_input == "Greedy":
            return "Two Player"
        elif self.text_input == "Two Player":
            return "Minimax"
        elif self.text_input == "Default Positions":
            return "User Positions"
        elif self.text_input == "User Positions":
            return "Default Positions"
        else:
            return False

    def handle_gods_event(self):
        """
        :return: the updated god selection
        """
        if self.text_input == "Prometheus":
            return "Hephaestus"
        elif self.text_input == "Hephaestus":
            return "Demeter"
        elif self.text_input == "Demeter":
            return "Hermes"
        elif self.text_input in ["Hermes", "Select God"]:
            return "Prometheus"
        else:
            return None

    def handle_god_mode_event(self):
        """
        :return: the updated god_mode
        """
        if self.text_input == "None":
            return "Simple Gods"
        elif self.text_input == "Simple Gods":
            return "Custom"
        elif self.text_input == "Custom":
            return "None"
