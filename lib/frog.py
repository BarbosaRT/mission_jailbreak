import pygame

import engine as e
from imports import load_image


class Frog:
    def __init__(self, x, y):
        self.entity = e.entity(x, y, 13, 13, 'frog')
        self.y_momentum = 0
        self.collision_types = {}
        self.x = 0
        self.y = 0
        self.movement = [0, 0]
        self.rect = self.entity.get_current_img().get_rect()
        self.life = 1
        self.attack_frame = -1
        self.direction = 1
        self.attack_images = []
        for _ in range(0, 10):
            self.attack_images.append(load_image('images/entities/frog/damage/damage_0.png', True))

    def attack(self):
        self.attack_frame = 9
        self.life -= 1

    def update(self, display: pygame.Surface, scroll, dt, tile_rects, ramps_rects):
        self.rect = self.entity.rect()
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1] + 16 + display.get_height()

        horizontal_condition = display.get_width() > self.rect.centerx > 0
        vertical_condition = display.get_height() > self.rect.centery > 0

        if horizontal_condition and vertical_condition:
            # for ramp in ramps_rects:
            #     if self.entity.rect().colliderect(ramp[0]):
            #         self.direction *= -1

            self.movement = [0, 0]
            if self.direction > 1:
                self.entity.set_flip(False)
                self.movement[0] = 1.5
            else:
                self.entity.set_flip(True)
                self.movement[0] = -1.5
            if self.y_momentum >= 3:
                self.y_momentum = 3
            self.movement[1] += self.y_momentum * dt
            self.y_momentum += 0.2 * dt

            # print(self.y_momentum)

            # VERIFICA AS COLISOES ---------------------------------------------------------------------- #
            self.collision_types = self.entity.move(self.movement, tile_rects, ramps=ramps_rects)

            if self.collision_types['bottom']:
                self.y_momentum = -5
                self.entity.set_action('idle')
            else:
                self.entity.set_action('jump')

        self.x = self.entity.x
        self.y = self.entity.y

        # self.entity.display(display, scroll)
        self.entity.change_frame(1)
        display.blit(self.entity.get_current_img(), self.rect)
        # pos = (self.x - scroll[0], self.y - scroll[1])

        # if self.attack_frame < 0:
        #     self.entity.display(display, scroll)
        #     self.entity.change_frame(1)
        #     display.blit(self.entity.get_current_img(), pos)
        # else:
        #     image = self.attack_images[self.attack_frame]
        #     if self.direction < 1:
        #         image = pygame.transform.flip(image, True, False)
        #     display.blit(image, pos)
        #     self.attack_frame -= 1
