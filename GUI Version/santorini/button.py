import pygame

from santorini.constants import button_icon

pygame.init()
font = pygame.font.SysFont("calibre", 30)
button_image = pygame.transform.scale(button_icon, (100, 40))


class Button:
    def __init__(self, x_pos, y_pos, text_input):
        self.image = button_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "orange")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    def check_input(self, position, mode):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if mode == "move":
                return "build"
            else:
                return "move"
        else:
            return mode

    def change_colour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = font.render(self.text_input, True, "orange")
        else:
            self.text = font.render(self.text_input, True, "white")
