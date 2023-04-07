import pygame
from pygame.locals import *
import sys

from imports import load_image


def rotate(pivot, orig_image, angle, width: float = 0, height: float = 0, pos=(0, 0)):
    if width == 0:
        width = orig_image.get_width()
    if height == 0:
        height = orig_image.get_height()

    cop_image = pygame.Surface((width, height))
    cop_image.fill((255, 255, 252))
    cop_image.set_colorkey((255, 255, 252))
    cop_image.blit(orig_image, pos)
    rot_image = pygame.transform.rotozoom(cop_image.convert_alpha(), angle, 1)
    rot_image_rect = rot_image.get_rect(center=pivot)
    return rot_image, rot_image_rect


def main():
    global image_clone, image_rect_clone
    angle = 0

    while 1:
        game_display = pygame.Surface((WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
        game_display.fill('#0996DB')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Angle
        angle += 1
        v = angle + 90

        pivot = image_rect.center
        image_clone, image_rect_clone = rotate(pivot, image, v, height=image.get_height() * 2)

        # Draws
        game_display.blit(image_clone, image_rect_clone)

        # Points
        pygame.draw.circle(game_display, (255, 255, 0), image_rect.center, 3)

        # Manages Window
        pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()), screen)
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    # PyGame Info ------------------------------------------------------ #
    WINDOW_SIZE = (800, 600)
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Template')
    screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)

    # Images ------------------------------------------------------------------ #
    image = load_image('../assets/arrow.png', True)
    image.set_colorkey((255, 255, 255))
    image_rect = image.get_rect(topright=(WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 5))

    image_clone = image.copy()
    image_rect_clone = image_clone.get_rect(topright=(WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 4))
    main()
