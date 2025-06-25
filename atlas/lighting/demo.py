import pygame
import pygame.gfxdraw
from pygame.locals import *
import sys
import math
import numpy
from atlas.lighting.raycaster import shoot_ray

# PyGame Info ------------------------------------------------------ #
WINDOW_SIZE = [800, 600]
GAME_SIZE = [800, 600]
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Rays')
screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)

# Variables ---------------------------------------------------------- #
GRAY = pygame.Color(39, 39, 39)  # 002277
GRAY_2 = pygame.Color(20, 20, 20)
GREEN = pygame.Color(0, 156, 59)  # 009C3B
YELLOW = pygame.Color(255, 223, 0)  # FFDF00
WHITE = pygame.Color(255, 255, 255)  # FFFFFF
ORANGE = pygame.Color(205, 75, 0)

LIMIT = int(math.sqrt(math.pow(GAME_SIZE[0], 2) + math.pow(GAME_SIZE[1], 2)))  # You can change it
BORDERS = 0  # The size of the circle borders
ACCURACY = 1  # Bigger values, less accuracy
CIRCLES = 5  # Number of circles to be drawn
NUM_LINES = 7200  # Number of lines
DRAW_LINES = False  # Draws the ray lines
ORIGIN = [400, 300]
FOV = 90
START_ANGLE = 45


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


def create_texture(image, size):
    texture = pygame.transform.smoothscale(image, size)
    return texture.copy()


def create_rays(num_lines, start_angle, fov):
    lines = []
    for i in range(num_lines):
        angle = math.radians(start_angle + fov / NUM_LINES * i)
        lines.append([angle, math.cos(angle), math.sin(angle)])
    return lines


angles = create_rays(NUM_LINES, START_ANGLE, FOV)
bulb = create_rays(360, 0, 361)

# Textures --------------------------------------------------------------------- #
TEXTURE1 = pygame.image.load('../assets/radial.png').convert_alpha()
NO_SHADOW_TEXTURE1 = pygame.Surface(GAME_SIZE)

TEXTURE2 = fill(TEXTURE1, ORANGE)
bulb_texture = create_texture(TEXTURE2, (LIMIT//2, LIMIT//2))
TEXTURE = create_texture(TEXTURE2, (LIMIT, LIMIT))
# bulb_texture = TEXTURE1


def create_rects(size, color, width=0):
    rectangle = pygame.Surface(size)
    rect = pygame.Rect(0, 0, size[0], size[1])
    pygame.draw.rect(rectangle, color, rect, width)
    rectangle.set_colorkey((0, 0, 0))
    mask = pygame.mask.from_surface(rectangle)
    return rectangle, mask


# Create the masks
def create_masks(color, width=0):
    top_rectangle, top_mask = create_rects((GAME_SIZE[0], 50), color, width)
    left_rectangle, left_mask = create_rects((50, GAME_SIZE[1]), color, width)
    masks = []
    x_pos = [[-150, 0], [0, 550]]
    y_pos = [[0, 0], [750, 0]]
    for p in x_pos:
        masks.append({'mask': top_mask, 'position': p, 'image': top_rectangle})
    for p in y_pos:
        masks.append({'mask': left_mask, 'position': p, 'image': left_rectangle})
    return masks


all_masks = create_masks(GRAY_2, BORDERS)

# Create the surfarray (numpy.ndarray) of the screen
# It basically combines all the masks into an image, and then transform the image to an array
mask_surface = pygame.Surface(GAME_SIZE)
mask_surface.set_colorkey('#000000')
for MASK in all_masks:
    position = MASK['position']
    mask_surf = MASK['mask'].to_surface()
    mask_surf.set_colorkey('#000000')
    mask_surface.blit(mask_surf, position)
array = pygame.surfarray.pixels2d(mask_surface).astype(dtype=numpy.int32)


# As the name implies this function shoots the rays
def shoot_rays(origin, lines, limit, texture, size, shadow, a, display):
    points = [origin]
    x, y = origin
    texture_rect = pygame.Rect(0, 0, texture.get_width(), texture.get_height())
    texture_rect.center = origin
    shadow.fill((0, 0, 0))
    shadow.blit(texture, texture_rect)

    for line in lines:
        # Calculates the distance
        distance = shoot_ray(x, y, line[0], limit, a, 1)
        # Calculates here it hits
        point = [int(origin[0] + line[1] * distance),
                 int(origin[1] + line[2] * distance)]
        points.append(point)
    polygon = pygame.Surface(size)
    polygon.set_colorkey((0, 0, 0))
    pygame.gfxdraw.textured_polygon(polygon, points, shadow, 0, 0)
    if display:
        display.blit(polygon, (0, 0), special_flags=BLEND_RGBA_ADD)


def return_surf(origin):
    game_display = pygame.Surface(GAME_SIZE)
    game_display.set_colorkey(0)
    shoot_rays(origin, angles, LIMIT, TEXTURE, GAME_SIZE, NO_SHADOW_TEXTURE1, array, game_display)
    return game_display


def main():
    global ORIGIN
    scale = (GAME_SIZE[0] / WINDOW_SIZE[0], GAME_SIZE[1] / WINDOW_SIZE[1])
    while 1:
        game_display = pygame.Surface(GAME_SIZE)
        game_display.fill(GRAY)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Draws
        # origin = [400, 100]
        origin = pygame.mouse.get_pos()
        ORIGIN = origin
        # THIS NEEDS TO BE INTEGER or else it won't work
        origin = (int(origin[0] * scale[0]), int(origin[1] * scale[1]))

        # Shoot Rays
        shoot_rays(origin, angles, LIMIT, TEXTURE, GAME_SIZE, NO_SHADOW_TEXTURE1, array, game_display)
        shoot_rays(origin, bulb, 20, bulb_texture, GAME_SIZE, NO_SHADOW_TEXTURE1, array, game_display)

        for mask in all_masks:
            game_display.blit(mask['image'], mask['position'])
        pygame.draw.circle(game_display, WHITE, origin, 5)

        # Manages Window
        pygame.display.set_caption(f'Rays: {clock.get_fps()}')
        pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()), screen)
        clock.tick(120)
        pygame.display.update()


if __name__ == '__main__':
    main()
