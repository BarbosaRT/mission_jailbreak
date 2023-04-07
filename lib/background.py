import pygame
from lib.imports import load_image


def resize(image, scale):
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))


def create_rect(surf, top, pos):
    return surf.get_rect(topleft=[surf.get_width() + pos, top])


SKY = load_image('images/background/1.png')
background_images = [
    resize(load_image('images/background/2.png', True), 0.5),
    resize(load_image('images/background/3.png', True), 0.5),
    resize(load_image('images/background/4.png', True), 0.5),
    resize(load_image('images/background/5.png', True), 0.5),
    resize(load_image('images/background/6.png', True), 0.5)
]

backgrounds = [
    [0.2, create_rect(background_images[0], 38, 0), background_images[0]],
    [0.3, create_rect(background_images[1], 38, 0), background_images[1]],
    [0.4, create_rect(background_images[2], 38, 0), background_images[2]],
    [0.5, create_rect(background_images[3], 38, 0), background_images[3]],
    [0.6, create_rect(background_images[4], 38, 0), background_images[4]]
]


def background(display, scroll):
    # BACKGROUND
    back = pygame.transform.scale(SKY, display.get_size())
    display.blit(back, (0, 0))

    for background_index in range(0, len(backgrounds)):
        speed = backgrounds[background_index][0]
        pos = backgrounds[background_index][1]
        objs = backgrounds[background_index][2]
        rect_obj = pygame.Rect(pos[0] - scroll[0] * speed, pos[1], pos[2], pos[3])

        if rect_obj.right < 0:
            display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
            v = pos[0] + objs.get_rect().width * 2
            backgrounds[background_index][1][0] = v
        if rect_obj.left - objs.get_rect().width * 2 > display.get_width():
            v = pos[0] - objs.get_rect().width * 2
            backgrounds[background_index][1][0] = v

        display.blit(objs, (rect_obj.x - objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 2, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 3, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 4, rect_obj.y))
        display.blit(objs, rect_obj)
        display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x + objs.get_rect().width * 2, rect_obj.y))
