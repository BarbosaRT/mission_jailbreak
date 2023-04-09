import math

import pygame
from pygame import Vector2
import engine as e
from lib.entities import bullet_group, Bullet
from lib.imports import load_image


class Guard:
    def __init__(self, x, y):
        self.entity = e.entity(x, y, 32, 32, 'guard')
        self.collision_types = {}
        self.x = x
        self.y = y
        self.rect = self.entity.get_current_img().get_rect()
        self.life = 4
        self.gun_angle = 0
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.hit_sound.set_volume(0.69)
        self.gun_pos = Vector2(0, 0)
        self.attack_frame = -1
        self.shooting = 0
        self.damage_images = []
        for _ in range(0, 16):
            self.damage_images.append(load_image('images/entities/guard/damage/damage.png', True))

    def damage(self):
        if self.attack_frame < 0:
            self.hit_sound.play()
            self.attack_frame = 15
            self.life -= 1

    def enemy_ia(self, scroll):
        # ATIRAR -------------------------------------------------------- #
        if self.shooting <= 0:
            self.gun_pos = [self.rect.centerx + scroll[0], self.rect.centery + scroll[1]]
            bullet_group.add(Bullet([self.x + 6, self.y + 22], self.gun_angle + 180, self))
            self.shooting = 10

    def update(self, display: pygame.Surface, scroll, player):
        if self.life <= 0:
            self.rect = pygame.Rect(0, 0, 0, 0)
            return
        self.rect = self.entity.rect()
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display_r = display.get_rect()

        if display_r.colliderect(self.rect):
            self.enemy_ia(scroll)
            if self.shooting > 0:
                self.shooting -= 0.1
            else:
                self.entity.set_action('idle')

            self.entity.set_flip(player.x < self.x)

            mx, my = player.x - scroll[0], player.y - scroll[1] + 22

            dx, dy = mx - self.rect.centerx, my - self.rect.centery
            self.gun_angle = math.degrees(math.atan2(dx, dy)) - 92

        if self.attack_frame < 0:
            self.entity.display(display, scroll)
            self.entity.change_frame(1)
        else:
            image = self.damage_images[self.attack_frame]
            if player.x < self.entity.x:
                image = pygame.transform.flip(image, True, False)
            display.blit(image, (self.x - scroll[0], self.y - scroll[1]))
            self.attack_frame -= 1
