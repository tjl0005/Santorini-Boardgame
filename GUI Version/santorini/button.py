import pygame

from .constants import button_icon

pygame.init()
font = pygame.font.SysFont("calibre", 30)


class Button:
    def __init__(self, x_pos, y_pos, text_input, button_size):
        self.image = pygame.transform.scale(button_icon, button_size)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "orange")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    def check_mode(self, position, mode):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if mode == "move":
                return "build"
            elif mode == "build":
                return "move"
            else:
                return None
        else:
            return mode

    def check_display(self, position, state):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if self.text_input == "Start":
                return "play"
            elif self.text_input == "Options":
                return "options"
            else:
                exit()
        else:
            return state

    def check_options(self, position, option_type):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if option_type == "start":
                return True
            elif option_type == "minimax":
                return "two"
            else:
                return "minimax"

    def change_colour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = font.render(self.text_input, True, "orange")
        else:
            self.text = font.render(self.text_input, True, "white")
