import math

import pygame

class Bulb:
    def __init__(self, pos):
        self.pos = pos

        self.num_lines = 360  # Number of lines
        self.fov = 90
        self.start_angle = 45

        angles = self.create_rays(self.num_lines, self.start_angle, self.fov)
        bulb = self.create_rays(360, 0, 361)

        # Textures --------------------------------------------------------------------- #
        self.TEXTURE1 = pygame.image.load('./atlas/assets/radial.png').convert_alpha()

    def create_rays(self, num_lines, start_angle, fov):
        lines = []
        for i in range(num_lines):
            angle = math.radians(start_angle + fov / self.num_lines * i)
            lines.append([angle, math.cos(angle), math.sin(angle)])
        return lines

    def create_texture(self, image, size):
        texture = pygame.transform.smoothscale(image, size)
        return texture.copy()

    def fill(self, surf, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        surface = surf.copy()
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))
        return surface
    def update(self, display, scroll, mask):
        game_size = display.get_size()

        ORANGE = pygame.Color(205, 75, 0)

        LIMIT = int(math.sqrt(math.pow(game_size[0], 2) + math.pow(game_size[1], 2)))  # You can change it

        NO_SHADOW_TEXTURE1 = pygame.Surface(game_size)

        # TEXTURE2 = self.fill(self.TEXTURE1, ORANGE)
        # bulb_texture = self.create_texture(TEXTURE2, (LIMIT // 2, LIMIT // 2))
        # TEXTURE = self.create_texture(TEXTURE2, (LIMIT, LIMIT))

        pos = [self.pos[0] - scroll[0], self.pos[1] - scroll[1]]
        rect = pygame.Rect(pos[0], pos[1], 10, 10)
        pygame.draw.rect(display, "red", rect)
