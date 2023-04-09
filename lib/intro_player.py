import pygame

import engine as e


class IntroPlayer:
    def __init__(self, x, y):
        self.entity = e.entity(x, y, 13, 13, 'player')
        self.x = x
        self.y = y
        self.entity.set_action('run')

    def update(self, screen, scroll):
        display = pygame.Surface((screen.get_width(), screen.get_height()))
        self.entity.display(display, scroll)
        self.entity.change_frame(1)
        current_img = self.entity.get_current_img()

        screen.blit(current_img, (self.x - scroll[0], self.y - scroll[1]))
