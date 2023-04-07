import math

import engine
from lib.imports import load_image


class PickupGun:
    def __init__(self, pos):
        self.pos = pos
        self.pickuped = False
        self.image = load_image('images/entities/enemy_down.png', True)
        self.image.set_colorkey(engine.e_colorkey)
        self.gun = load_image('images/guns/spy_gun_pickup.png', True)
        self.gun.set_colorkey(engine.e_colorkey)
        self.time_passed = 0

    def update(self, display, scroll, dt, player):
        local_pos = [self.pos[0] - scroll[0], self.pos[1] - scroll[1]]
        if not self.pickuped:
            self.time_passed += dt / 20
            gun_pos = local_pos.copy()
            gun_pos[0] += 8
            gun_pos[1] += math.sin(self.time_passed) * 6

            gun_rect = self.gun.get_rect(topleft=gun_pos)
            local_player_rect = player.rect.copy()
            local_player_rect.x -= scroll[0]
            local_player_rect.y -= scroll[1] - 16

            display.blit(self.gun, gun_rect)
            if gun_rect.colliderect(local_player_rect):
                player.is_gun_enabled = True
                self.pickuped = True

        display.blit(self.image, local_pos)
