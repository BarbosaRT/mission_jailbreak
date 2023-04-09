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
    [0.2, create_rect(background_images[0], 45, 0), background_images[0]],
    [0.3, create_rect(background_images[1], 45, 0), background_images[1]],
    [0.4, create_rect(background_images[2], 45, 0), background_images[2]],
    [0.5, create_rect(background_images[3], 45, 0), background_images[3]],
    [0.6, create_rect(background_images[4], 45, 0), background_images[4]]
]

SKY_2 = load_image('images/background_2/1.png')
background_images_2 = [
    resize(load_image('images/background_2/2.png', True), 0.75),
    resize(load_image('images/background_2/3.png', True), 0.75),
    resize(load_image('images/background_2/4.png', True), 0.75),
    resize(load_image('images/background_2/5.png', True), 0.75),
]

backgrounds_2 = [
    [0.2, create_rect(background_images_2[0], -25, 0), background_images_2[0]],
    [0.3, create_rect(background_images_2[1], -25, 0), background_images_2[1]],
    [0.4, create_rect(background_images_2[2], -25, 0), background_images_2[2]],
    [0.5, create_rect(background_images_2[3], -25, 0), background_images_2[3]],
]

SKY_3 = load_image('images/clouds/1.png')
background_images_3 = [
    resize(load_image('images/clouds/2.png', True), 0.5),
    resize(load_image('images/clouds/3.png', True), 0.5),
    resize(load_image('images/clouds/4.png', True), 0.5),
]

backgrounds_3 = [
    [0.3, create_rect(background_images_3[0], 30, 0), background_images_3[0]],
    [0.5, create_rect(background_images_3[1], 30, 0), background_images_3[1]],
    [0.7, create_rect(background_images_3[2], 30, 0), background_images_3[2]],
]


def background_3(display, scroll, enable_vertical=False):
    # BACKGROUND
    back = pygame.transform.scale(SKY_3, display.get_size())
    display.blit(back, (0, 0))

    for background_index in range(0, len(backgrounds_3)):
        speed = backgrounds_3[background_index][0]
        pos = backgrounds_3[background_index][1]
        objs = backgrounds_3[background_index][2]
        vertical = pos[1] - scroll[1] * speed if enable_vertical else pos[1]
        rect_obj = pygame.Rect(pos[0] - scroll[0] * speed, vertical, pos[2], pos[3])

        if rect_obj.right < 0:
            display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
            v = pos[0] + objs.get_rect().width * 2
            backgrounds_3[background_index][1][0] = v
        if rect_obj.left - objs.get_rect().width * 2 > display.get_width():
            v = pos[0] - objs.get_rect().width * 2
            backgrounds_3[background_index][1][0] = v

        display.blit(objs, (rect_obj.x - objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 2, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 3, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 4, rect_obj.y))
        display.blit(objs, rect_obj)
        display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x + objs.get_rect().width * 2, rect_obj.y))


def background_2(display, scroll, enable_vertical=False):
    # BACKGROUND
    back = pygame.transform.scale(SKY_2, display.get_size())
    display.blit(back, (0, 0))

    for background_index in range(0, len(backgrounds_2)):
        speed = backgrounds_2[background_index][0]
        pos = backgrounds_2[background_index][1]
        objs = backgrounds_2[background_index][2]
        vertical = pos[1] - scroll[1] * speed if enable_vertical else pos[1]
        rect_obj = pygame.Rect(pos[0] - scroll[0] * speed, vertical, pos[2], pos[3])

        if rect_obj.right < 0:
            display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
            v = pos[0] + objs.get_rect().width * 2
            backgrounds_2[background_index][1][0] = v
        if rect_obj.left - objs.get_rect().width * 2 > display.get_width():
            v = pos[0] - objs.get_rect().width * 2
            backgrounds_2[background_index][1][0] = v

        display.blit(objs, (rect_obj.x - objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 2, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 3, rect_obj.y))
        display.blit(objs, (rect_obj.x - objs.get_rect().width * 4, rect_obj.y))
        display.blit(objs, rect_obj)
        display.blit(objs, (rect_obj.x + objs.get_rect().width, rect_obj.y))
        display.blit(objs, (rect_obj.x + objs.get_rect().width * 2, rect_obj.y))


def background(display, scroll, enable_vertical=False):
    # BACKGROUND
    back = pygame.transform.scale(SKY, display.get_size())
    display.blit(back, (0, 0))

    for background_index in range(0, len(backgrounds)):
        speed = backgrounds[background_index][0]
        pos = backgrounds[background_index][1]
        objs = backgrounds[background_index][2]
        vertical = pos[1] - scroll[1] * speed if enable_vertical else pos[1]
        rect_obj = pygame.Rect(pos[0] - scroll[0] * speed, vertical, pos[2], pos[3])

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
