import pygame

from ..constants import button_icon, squirk

pygame.init()
font = pygame.font.Font(squirk, 20)


class Button:
    def __init__(self, x_pos, y_pos, text_input, button_size):
        self.image = pygame.transform.scale(button_icon, button_size)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.hovered = False

    def update(self):
        if self.hovered:
            self.text = font.render(self.text_input, True, "lightblue")
        else:
            self.text = font.render(self.text_input, True, "white")

    def draw(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    def update_text(self, text):
        self.text_input = text
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.update()

    def handle_event(self, event, button_type):
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
                    if self.text_input == "back":
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

    def check_mode(self, position, mode):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if mode == "moving":
                return "building"
            elif mode == "building":
                return "moving"
            else:
                return None
        else:
            return mode
