"""
Contains the button class used to create button objects with functionality
"""
import pygame

from ..utils.assets import BUTTON_ICON, SQUIRK

pygame.init()
font = pygame.font.Font(SQUIRK, 20)


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
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.hovered = False  # User mouse on button

    def update(self):
        """
        Detect if user hovering over button and change text colour to reflect
        """
        if self.hovered:
            self.text = font.render(self.text_input, True, "lightblue")
        else:
            self.text = font.render(self.text_input, True, "white")

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
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.update()

    def handle_event(self, event, button_type):
        """
        Detect if button is being hovered over and also detect if a button is pressed. If a button is pressed perform
        given action
        :param event: pygame event
        :param button_type: origin of button e.g. option menu
        :return:
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                if button_type == "mode":
                    if self.text_input == "moving":
                        return "building"
                    elif self.text_input == "building":
                        return "moving"
                    else:
                        return "start"
                elif button_type == "display":
                    if self.text_input == "Start":
                        return "play"
                    elif self.text_input == "Options":
                        return "options"
                    else:
                        exit()
                elif button_type == "options":
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
                elif button_type == "confirm":
                    return True
