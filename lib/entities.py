
from pygame.math import Vector2

import pygame
import math


pygame.init()

bullet_group = pygame.sprite.Group()


def sign(value: int):
    return -1 if value < 0 else 1


def polar_angle(center, point):
    h = int(point[0] - center[0])
    v = int(point[1] - center[1])

    c_adj = math.fabs(h)
    c_oposto = math.fabs(v)

    if c_adj == 0:
        c_adj = 1

    # Without Angle Correction = math.atan(h / v)
    # Angle Correction
    m = sign(h) + sign(v)
    value = -360 if m == 2 else -180 if m == -2 else 0 if sign(h) == 1 else 180

    angle = math.fabs(math.radians(value) + math.atan(c_oposto / c_adj))
    return angle


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, who_shoot):
        super(Bullet, self).__init__()
        angle -= 180

        self.image = pygame.Surface([2, 2])
        self.who_shoot = who_shoot
        self.image.fill('yellow')
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=pos)
        # To apply an offset to the start position,
        # create another vector and rotate it as well.
        offset = Vector2(0, 0).rotate(-angle)

        # Use the offset to change the starting position.
        self.pos = Vector2(pos) + offset
        self.velocity = Vector2(5, 0)
        self.velocity.rotate_ip(angle)
        self.velocity.y = -self.velocity.y

    def update(self, display: pygame.Surface, scroll, enemies, tile_rects, ramps_rects):
        self.rect = self.image.get_rect(center=self.pos)
        self.pos += self.velocity
        self.rect.center = self.pos
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        if self.rect.right - scroll[0] <= 0 or self.rect.bottom - scroll[1] <= 0 or \
                self.rect.top - scroll[1] >= display.get_height() or self.rect.left - scroll[0] >= display.get_width():
            self.kill()

        if ramps_rects:
            if self.ramp_collision(ramps_rects):
                self.kill()
        if tile_rects:
            if self.tile_collision(tile_rects):
                self.kill()

        if enemies:
            col_eny = self.collision_test(display, enemies, scroll)
            if col_eny:
                for enemy in col_eny:
                    enemy.damage()
                    if enemy.life == 0:
                        enemies.remove(enemy)
                    self.kill()

    def tile_collision(self, rects):
        r = self.rect.copy()
        r.y -= 16
        for rect in rects:
            if r.colliderect(rect):
                return True
        return False

    def ramp_collision(self, rects):
        r = self.rect.copy()
        r.y -= 16
        for rect in rects:
            if r.colliderect(rect[0]):
                return True
        return False

    def collision_test(self, display, rects, scroll):
        output = []
        r = self.rect.copy()
        r.x -= scroll[0]
        r.y -= scroll[1]
        for rect in rects:
            local_rect = rect.rect
            if rect.entity.type == self.who_shoot.entity.type:
                continue
            if rect.entity.type == "player":
                local_rect.x -= scroll[0]
                local_rect.y -= scroll[1] - 16
            if r.colliderect(rect.rect):
                output.append(rect)
        return output



