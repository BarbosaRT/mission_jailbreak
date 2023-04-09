import random

import pygame

import engine as e
from lib.imports import load_image


class Frog:
    def __init__(self, x, y):
        self.entity = e.entity(x, y, 13, 13, 'frog')
        self.y_momentum = 0
        self.collision_types = {}
        self.x = 0
        self.y = 0
        self.speed = random.randint(1, 2)
        self.movement = [0.0, 0.0]
        self.rect = self.entity.get_current_img().get_rect()
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.hit_sound.set_volume(0.69)
        self.life = 2
        self.attack_frame = -1
        self.direction = 1
        self.attack_images = []
        for _ in range(0, 10):
            self.attack_images.append(load_image('images/entities/frog/damage/damage_0.png', True))

    def damage(self):
        if self.attack_frame < 0:
            self.hit_sound.play()
            self.attack_frame = 9
            self.life -= 1

    def update(self, display: pygame.Surface, scroll, dt, tile_rects, ramps_rects, player):
        if self.life <= 0:
            self.rect = pygame.Rect(0, 0, 0, 0)
            return
        self.rect = self.entity.rect().copy()
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1] - 16

        display_r = display.get_rect()
        display_r.height += 96
        display_r.y -= 64

        if display_r.colliderect(self.rect):
            self.movement[1] = 0
            if self.direction >= 1:
                self.entity.set_flip(False)
                self.movement[0] = self.speed
            else:
                self.entity.set_flip(True)
                self.movement[0] = -self.speed
            if self.y_momentum >= 3:
                self.y_momentum = 3
            self.movement[1] += self.y_momentum * dt
            self.y_momentum += 0.2 * dt

            # VERIFICA AS COLISOES ---------------------------------------------------------------------- #
            self.collision_types = self.entity.move(self.movement, tile_rects, ramps=ramps_rects)

            if self.collision_types['left'] or self.collision_types['right']:
                self.direction *= -1

            if self.collision_types['bottom']:
                self.y_momentum = -4
                self.entity.set_action('idle')
            else:
                self.entity.set_action('jump')

        self.x = self.entity.x
        self.y = self.entity.y
        pos = (self.x - scroll[0], self.y - scroll[1] + 16)

        if self.entity.rect().colliderect(player.rect):
            player.damage()

        if self.attack_frame < 0:
            if self.life <= 1:
                self.life -= 1
            self.entity.change_frame(1)
            display.blit(self.entity.get_current_img(), pos)
        else:
            image = self.attack_images[self.attack_frame]
            if self.direction < 1:
                image = pygame.transform.flip(image, True, False)
            display.blit(image, pos)
            self.attack_frame -= 1

