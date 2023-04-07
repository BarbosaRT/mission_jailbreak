import pygame
from atlas.UI.essentials import create_surf
from atlas.UI.text import Text


class Button:
    def __init__(self, x, y, width=50, height=10, color=pygame.Color(200, 200, 200, 155),
                 highlight_color=pygame.Color(150, 150, 150, 155), text='Button', font=pygame.font.Font(None, 30),
                 reference=(1280, 720), border_radius=5):
        self.x = x
        self.y = y
        self.color = color
        self.highlight_color = highlight_color
        self.size = (width, height)
        self.rect = pygame.Rect(0, 0, self.x, self.y)
        self.text = text
        self.font = font
        self.current_color = color
        self.clicked = False
        self.font = font
        self.scale = [1, 1]
        self.reference = reference
        self.border_radius = border_radius

    def logic(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse[0], mouse[1]):
            clicked = pygame.mouse.get_pressed(3)[0]
            if clicked:
                self.clicked = True
                self.current_color = self.color
            else:
                self.clicked = False
                self.current_color = self.highlight_color
        else:
            self.current_color = self.color

    def update(self, display: pygame.Surface):
        # Get the scale for the object
        self.scale = (display.get_width() / self.reference[0], display.get_height() / self.reference[1])

        button = create_surf(self.size[0] * 3 * self.scale[0], self.size[1] * 3 * self.scale[1], self.current_color)
        self.rect = button.get_rect(topleft=(self.x, self.y))
        self.logic()

        text = Text(self.x, self.y, text=self.text, size=self.size, align='center')

        text.update(display, displays=False)
        pygame.draw.rect(display, self.current_color, self.rect, border_radius=self.border_radius)
        text.update(display)
