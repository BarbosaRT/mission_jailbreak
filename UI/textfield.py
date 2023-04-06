import pygame
from pygame.locals import *
from UI.essentials import create_surf
from UI.text import Text
pygame.font.init()


class TextField:
    def __init__(self, x, y, width=70, height=20, color=pygame.Color(150, 150, 150, 155),
                 highlight_color=pygame.Color(200, 200, 200, 155), font=pygame.font.Font(None, 30),
                 reference=(1280, 720), border_radius=5, outline=1, text_color=pygame.Color(0, 0, 0, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.highlight_color = highlight_color
        self.size = (width, height)
        self.rect = pygame.Rect(0, 0, self.x, self.y)
        self.text = 'Enter text'
        self.font = font
        self.current_color = color
        self.clicked = False
        self.selected = False
        self.font = font
        self.scale = [1, 1]
        self.reference = reference
        self.textobj = Text(self.x, self.y, color=text_color, size=self.size, text_pos=(5, 5))
        self.border_radius = border_radius
        self.outline = outline

    def event_logic(self, event):
        if self.selected:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE or event.key == K_DELETE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def logic(self):
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed(3)[0]
        if self.rect.collidepoint(mouse[0], mouse[1]):
            if clicked and not self.selected:
                if self.text == 'Enter text':
                    self.text = ''
                self.selected = True
        else:
            if clicked:
                self.selected = False

        self.current_color = self.highlight_color if self.selected else self.color

    def update(self, display: pygame.Surface):
        # Get the scale for the object
        self.scale = (display.get_width() / self.reference[0], display.get_height() / self.reference[1])

        textfield = create_surf(self.size[0] * 3 * self.scale[0], self.size[1] * 3 * self.scale[1], self.current_color)
        self.rect = textfield.get_rect(topleft=(self.x, self.y))
        self.logic()

        self.textobj.write(self.text)

        pygame.draw.rect(display, self.current_color, self.rect, width=self.outline, border_radius=self.border_radius)
        self.textobj.update(display)
