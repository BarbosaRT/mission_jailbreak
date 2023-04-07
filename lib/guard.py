import pygame
from pygame import Vector2


class Guard:
    def __init__(self, x, y, tag):
        self.entity = e.entity(x, y, 32, 32, tag)
        self.collision_types = {}
        self.x = x
        self.y = y
        self.rect = self.entity.get_current_img().get_rect()
        self.life = 4
        self.gun_angle = 0
        self.gun_pos = Vector2(0, 0)
        self.attack_frame = -1
        self.shooting = 0

    def attack(self):
        self.attack_frame = 9
        self.life -= 1

    def enemy_ia(self, scroll):
        # ATIRAR -------------------------------------------------------- #
        if self.shooting <= 0:
            self.gun_pos = [self.rect.centerx + scroll[0], self.rect.centery + scroll[1]]
            enemies.append(Cannon_Ball(self.gun_pos, self.gun_angle, len(enemies)))
            self.shooting = 20
            cannon.set_action('fire', force=True)

    def update(self, display: pygame.Surface, scroll, player):
        self.rect = self.entity.rect()
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display_r = display.get_rect()

        if display_r.colliderect(self.rect):
            self.enemy_ia(scroll)
            if self.shooting > 0:
                self.shooting -= 0.1
            else:
                cannon.set_action('idle')

            gun_rect = self.rect.copy()
            gun_copy = cannon.get_current_img().copy()
            gun_rect.x += scroll[0]
            gun_rect.y += scroll[1]
            mx, my = player.x, player.y
            rotated_gun, rotated_rect, self.gun_angle = rotate(gun_rect, gun_copy, mx, my, 1, 270)
            self.gun_pos = rotated_rect
            rotated_rect.y -= 5
            cannon.change_frame(1)

            display.blit(rotated_gun, (rotated_rect.x - scroll[0], rotated_rect.y - scroll[1]))

        if self.attack_frame < 0:
            self.entity.display(display, scroll)
            self.entity.change_frame(1)
        else:
            image = turret_damage[self.attack_frame]
            if player.x < self.entity.x:
                image = pygame.transform.flip(image, True, False)
            display.blit(image, (self.x - scroll[0], self.y - scroll[1]))
            self.attack_frame -= 1