import pygame


class Button:
    def __init__(self, x, y, width, height, color, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = font
        self.state = False

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (75, 75, 75))
        text_rext = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rext)

    def is_mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def toggle(self):
        self.state = not self.state