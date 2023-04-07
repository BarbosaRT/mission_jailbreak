import math

import numpy
import pygame
from pygame.locals import *

from atlas.lighting.raycaster import shoot_ray
from lib.imports import load_image
from math import *

def aaline(surface, color, start_pos, end_pos, width=1):
    """ Draws wide transparent anti-aliased lines. """
    # ref https://stackoverflow.com/a/30599392/355230

    x0, y0 = start_pos
    x1, y1 = end_pos
    midpnt_x, midpnt_y = (x0+x1)/2, (y0+y1)/2  # Center of line segment.
    length = hypot(x1-x0, y1-y0)
    angle = atan2(y0-y1, x0-x1)  # Slope of line.
    width2, length2 = width/2, length/2
    sin_ang, cos_ang = sin(angle), cos(angle)

    width2_sin_ang = width2*sin_ang
    width2_cos_ang = width2*cos_ang
    length2_sin_ang = length2*sin_ang
    length2_cos_ang = length2*cos_ang

    # Calculate box ends.
    ul = (midpnt_x + length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang + length2_sin_ang)
    ur = (midpnt_x - length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang - length2_sin_ang)
    bl = (midpnt_x + length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang + length2_sin_ang)
    br = (midpnt_x - length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang - length2_sin_ang)

    pygame.gfxdraw.aapolygon(surface, (ul, ur, br, bl), color)
    pygame.gfxdraw.filled_polygon(surface, (ul, ur, br, bl), color)


class Camera:
    def __init__(self, pos, start_angle=0, fov=60, blink=False, move=False):
        self.pos = pos
        self.image = load_image('images/entities/enemy.png', True)
        self.rect = self.image.get_rect(topleft=pos)
        self.dt = 0
        self.angle = 0
        self.start_angle = start_angle
        self.fov = fov
        self.isTouchingPlayer = False
        self.blink = blink
        self.time_passed = -20
        self.move = move

    def update(self, display, scroll, dt, mask_surface, player_rect: pygame.rect.Rect):
        self.dt = dt
        self.angle += dt / 120
        self.time_passed += dt
        if self.move:
            pos = list(self.pos)
            pos[0] += math.sin(self.angle * 2.5) * dt * 2.5
            self.pos = pos.copy()
        degree_angle = self.start_angle + math.sin(self.angle) * self.fov
        radians_angle = math.radians(-degree_angle + 90)

        rot_image = pygame.transform.rotozoom(self.image, degree_angle, 1)
        rot_image_rect = rot_image.get_rect(center=self.pos)
        game_size = display.get_size()
        local_pos = (rot_image_rect.x - scroll[0], rot_image_rect.y - scroll[1])
        center_pos = (rot_image_rect.centerx - scroll[0] + 1, rot_image_rect.centery - scroll[1])

        limit = int(math.sqrt(math.pow(game_size[0], 2) + math.pow(game_size[1], 2)))

        array = pygame.surfarray.pixels2d(mask_surface).astype(dtype=numpy.int32)

        # Calculates the distance
        distance = shoot_ray(center_pos[0], center_pos[1], radians_angle, limit, array, 1)

        # Calculates here it hits
        point = [int(center_pos[0] + math.cos(radians_angle) * distance),
                 int(center_pos[1] + math.sin(radians_angle) * distance)]

        collsion_point = [int(center_pos[0] + math.cos(radians_angle) * (distance - 10)),
                          int(center_pos[1] + math.sin(radians_angle) * (distance - 10))]
        local_player_rect = player_rect.copy()
        local_player_rect.x -= scroll[0]
        local_player_rect.y -= scroll[1] - 16

        is_showing = display.get_width() > center_pos[0] > -100 and display.get_height() > center_pos[1] > 0

        if self.time_passed > 200:
            self.time_passed = -50
        if self.blink:
            if self.time_passed > 0:
                if is_showing:
                    self.isTouchingPlayer = local_player_rect.collidepoint(collsion_point[0], collsion_point[1])
                    pygame.draw.aaline(display, "red", center_pos, point)
                    aaline(display, Color(255, 0, 0, 50), center_pos, point, width=3)

        elif display.get_width() > center_pos[0] > -100 and display.get_height() > center_pos[1] > 0:
            self.isTouchingPlayer = local_player_rect.collidepoint(collsion_point[0], collsion_point[1])
            pygame.draw.aaline(display, "red", center_pos, point)
            aaline(display, Color(255, 0, 0, 50), center_pos, point, width=3)

        display.blit(rot_image, local_pos)
