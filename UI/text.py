import pygame

pygame.font.init()


class Text:
    def __init__(self, x, y, text='', font_type=None, font_size=30, antialias=True, align='left',
                 color=(255, 255, 255), reference=(1280, 720), size=(50, 50), text_pos=(0, 0), spacing=-10):
        """
        :summary: A Text object that displays a text
        :param x: x position of the Text
        :param y: y position of the Text
        :param text: text to be displayed
        :param antialias: if will use antialias
        :param color: color of the text
        :param reference: reference resolution (used for scaling)
        """
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_type, font_size)
        self.antialias = antialias
        self.surface_rect = pygame.Rect(0, 0, 0, 0)
        self.color = pygame.Color(color[0], color[1], color[2], 10)
        self.reference = reference
        self.scale = (0, 0)
        self.label = []
        self.size = size
        self.font_size = font_size
        self.textpos = list(text_pos)
        self.spacing = spacing
        self.align = align
        self.text = ''
        self.write(text)

    def write(self, input_text: str):
        label = []
        text = input_text.split('\r')
        for line in text:
            label.append(self.font.render(line, self.antialias, self.color))
        self.label = label
        self.text = input_text

    def update(self, display, displays=True):
        # Get the scale for the object
        self.scale = (display.get_width() / self.reference[0], display.get_height() / self.reference[1])

        # Create the text surface
        original_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)

        # Alignments
        if self.align.upper() == 'CENTER':
            self.textpos[0] = original_surface.get_width() / 2 - self.font.size(self.text)[0] / 2
            self.textpos[1] = original_surface.get_height() / 2 - self.font.size(self.text)[1] / 2

        for line in range(len(self.label)):
            word = self.label[line]
            original_surface.blit(word, (self.textpos[0], self.textpos[1] + line * (self.font_size + self.spacing)))

        # Scale the text surface
        surface = pygame.transform.scale(original_surface, (int(original_surface.get_width() * self.scale[0]),
                                                            int(original_surface.get_height() * self.scale[1])))

        # Create a Rect For the Surface
        self.surface_rect = surface.get_rect(topleft=(self.x, self.y))

        # Display The Text
        if displays:
            display.blit(surface, self.surface_rect)
