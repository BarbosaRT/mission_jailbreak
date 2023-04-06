import math

import numpy
import pygame
import pygame.gfxdraw

from atlas.lighting.demo import shoot_rays, return_surf
from atlas.lighting.raycaster import shoot_ray

pygame.init()


def fill(surf, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    surface = surf.copy()
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))
    return surface


class Ray:
    def __init__(self, origin, fov, start_angle, color, size, lines=1800, limit=100):
        self.limit = limit
        self.fov = fov
        self.start_angle = start_angle
        self.origin = origin
        self.color = color
        self.lines = lines
        self.angles = self.create_rays(self.lines, self.start_angle, self.fov)

        # Textures --------------------------------------------------------------------- #
        self.texture1 = pygame.image.load('./atlas/assets/radial.png').convert_alpha()
        self.texture1.set_colorkey(0)
        self.no_shadow_texture1 = pygame.Surface(size)
        self.no_shadow_texture1.set_colorkey(0)
        self.texture2 = fill(self.texture1, self.color)
        self.texture = self.create_texture(self.texture2, [self.limit, self.limit])

    @staticmethod
    def create_texture(image, size):
        texture = pygame.transform.smoothscale(image, size)
        return texture.copy()

    def create_rays(self, num_lines, start_angle, fov):
        lines = []
        for i in range(num_lines):
            angle = math.radians(start_angle + fov / self.lines * i)
            lines.append([angle, math.cos(angle), math.sin(angle)])
        return lines

    def render(self, display: pygame.Surface, mask: pygame.Surface):
        # mask_surface = pygame.mask.from_surface(mask).to_surface()
        # array = pygame.surfarray.pixels2d(mask_surface).astype(dtype=numpy.int32)
        # display.blit(mask_surface, (0, 0))
        # shoot_rays(self.origin, self.angles, self.limit, self.texture, display.get_size(), self.no_shadow_texture1, array, display)
        # self.shoot_rays(array, self.angles, self.limit, self.texture, display.get_size(), display)
        display.blit(return_surf(self.origin), (0, 0))

    """# As the name implies this function shoots the rays
    def shoot_rays(self, array, angles, limit, texture, size, display=None):
        points = [self.origin]
        x, y = self.origin
        texture_rect = pygame.Rect(0, 0, texture.get_width(), texture.get_height())
        texture_rect.center = self.origin
        self.no_shadow_texture1.fill((0, 0, 0))
        self.no_shadow_texture1.blit(texture, texture_rect)

        for line in angles:
            # Calculates the distance
            distance = shoot_ray(x, y, line[0], limit, array, 1)
            # Calculates here it hits
            point = [int(self.origin[0] + line[1] * distance),
                     int(self.origin[1] + line[2] * distance)]
            points.append(point)
        polygon = pygame.Surface(size)
        polygon.set_colorkey((0, 0, 0))
        pygame.gfxdraw.textured_polygon(polygon, points, self.no_shadow_texture1, 0, 0)
        if display:
            display.blit(polygon, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)"""
