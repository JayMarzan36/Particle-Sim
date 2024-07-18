import pygame


class Slider:
    def __init__(self, x, y, width, height, initial_value, min_value, max_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect((x - width // 2), (y - height // 2), width, height)
        self.buttonRect = pygame.Rect((x - width // 2) + initial_value - 5, (y - height // 2), 10, height)
        self.initial_value = ((x + width // 2) - (x - width // 2) * initial_value)
        self.min_value = min_value
        self.max_value = max_value

    def move_slider(self, mouse_pos):
        self.buttonRect.centerx = mouse_pos[0]

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        pygame.draw.rect(window, (100, 100, 100), self.buttonRect)

    def get_value(self):
        val_range = (self.x + self.width // 2) - (self.x - self.width)
        button_val = (self.buttonRect.centerx - self.x - self.width)
        return (button_val / val_range) * (self.max_value - self.min_value) + self.min_value

    def is_mouse_over_button(self):
        return self.buttonRect.collidepoint(pygame.mouse.get_pos())

    def is_mouse_over_slider(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())