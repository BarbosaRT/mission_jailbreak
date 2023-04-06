import pygame


def create_surf(x, y, color):
    surf = pygame.Surface([x, y])
    if color.a != 255:
        surf.set_alpha(color.a)
    surf.fill(color)
    return surf
