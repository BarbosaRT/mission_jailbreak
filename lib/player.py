import engine as e
import pygame
from pygame.locals import *
import random
import math

from lib.entities import bullet_group, Bullet, polar_angle


class Player:
    def __init__(self, x, y, tag):
        self.collision_types = {}
        self.entity = e.entity(x, y, 13, 24, tag)
        self.x = x
        self.y = y
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.vertical_momentum = -5
        self.air_timer = 0
        self.grass_sound_timer = 0
        self.player_movement = [0, 0]
        self.shoot_sound = pygame.mixer.Sound('./audio/shoot_2.wav')
        self.shoot_sound.set_volume(0.69)
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.hit_sound.set_volume(0.69)
        self.jump_sound = pygame.mixer.Sound('./audio/jump.wav')
        self.jump_sound.set_volume(0.69)
        self.grass_sounds = [pygame.mixer.Sound('./audio/step_1.ogg'), pygame.mixer.Sound('./audio/step_2.ogg')]
        self.grass_sounds[0].set_volume(0.5)
        self.grass_sounds[1].set_volume(0.5)
        self.rect = self.entity.rect()
        self.gun_angle = 0
        self.scroll = [0, 0]
        self.true_scroll = [0, 0]
        self.dt = 0
        self.keys = {
            'UP': [K_w, K_UP],
            'LEFT': [K_a, K_LEFT],
            'RIGHT': [K_d, K_RIGHT],
            'RESPAWN': [K_r]
        }
        self.guns = {
            'gun': ['images/guns/spy_gun.png', 20],
        }
        self.current_gun = 'gun'
        self.is_gun_enabled = False
        self.change_delay = 20
        self.gun_delay = self.change_delay
        self.checkpoint_pos = [220, 2800]
        self.life = 6
        self.damage_delay = 44
        self.final = False

    def key_verifier(self, key, keys):
        for k in self.keys[key]:
            if keys[k]:
                return True
        return False

    def damage(self):
        if self.life <= 0:
            return
        if self.damage_delay < 0:
            self.hit_sound.play()
            self.life -= 1
            self.damage_delay = 44

    def inputs(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed(3)
        if self.gun_delay > 0:
            self.gun_delay -= self.dt

        if mouse[0] and self.gun_delay <= 0 and self.is_gun_enabled:
            bullet_group.add(Bullet([self.x + 6, self.y + 22], self.gun_angle + 180, self))
            self.gun_delay = self.change_delay
            self.shoot_sound.play()
            self.scroll[0] += (random.randint(0, 4) - 2) * self.dt
            self.scroll[1] += (random.randint(0, 4) - 2) * self.dt
        # APERTOU O RESPAWN ---------------------------------------------------------- #
        if self.key_verifier('RESPAWN', keys):
            self.life = 0

        # APERTOU PARA PULAR --------------------------------------------------------- #
        if self.key_verifier('UP', keys):
            if self.air_timer < 6:
                if self.vertical_momentum >= 0:
                    self.jump_sound.play()
                if self.player_movement[0] > 0:
                    self.entity.set_action('jump_right')
                if self.player_movement[0] < 0:
                    self.entity.set_action('jump_left')

                self.vertical_momentum = -5

        # APERTOU PARA ESQUERDA ------------------------------------------------------ #
        if self.key_verifier('LEFT', keys):
            self.moving_left = True
        else:
            self.moving_left = False

        # APERTOU PARA DIREITA ------------------------------------------------------- #
        if self.key_verifier('RIGHT', keys):
            self.moving_right = True
        else:
            self.moving_right = False

    def update(self, screen, tile_rects, ramps_rects, dt, respawn_rects, final_rects):
        for respawn_rect in respawn_rects:
            if self.rect.colliderect(respawn_rect):
                self.life = 0
        for final_rect in final_rects:
            if self.rect.colliderect(final_rect):
                self.final = True

        if self.life <= 0:
            self.life = 6
            self.entity.set_pos(self.checkpoint_pos[0], self.checkpoint_pos[1])

        self.dt = dt
        self.true_scroll[0] += ((self.x - self.true_scroll[0] - screen.get_width() / 2) / 20) * dt
        self.true_scroll[1] += ((self.y - self.true_scroll[1] - screen.get_height() / 2) / 20) * dt
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
        if not self.final:
            self.inputs()
        self.rect = self.entity.rect()
        display = pygame.Surface((screen.get_width(), screen.get_height()))

        if self.grass_sound_timer > 0:
            self.grass_sound_timer -= 1

        self.player_movement = [0, 0]

        if self.dt == 0:
            self.dt = 1

        if self.moving_right:
            self.player_movement[0] += 2 * self.dt
        if self.moving_left:
            self.player_movement[0] -= 2 * self.dt

        self.player_movement[1] += self.vertical_momentum * self.dt
        self.vertical_momentum += 0.2 * self.dt
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

        # VERIFICA SE ESTÁ INDO PARA A DIREITA ------------------------------------------------------- #
        if self.player_movement[0] > 0:
            self.entity.set_flip(False)

        # VERIFICA SE ESTÁ INDO PARA A ESQUERDA ------------------------------------------------------ #
        if self.player_movement[0] < 0:
            self.entity.set_flip(True)

        # VERIFICA AS COLISOES ---------------------------------------------------------------------- #
        self.collision_types = self.entity.move(self.player_movement, tile_rects, ramps=ramps_rects)

        # VERIFICA SE ESTA NO CHAO ------------------------------------------------------------------ #
        if self.collision_types['bottom']:
            self.jump = False
            self.air_timer = 0
            self.vertical_momentum = 0
            if self.player_movement[0] != 0:
                if self.grass_sound_timer == 0:
                    self.grass_sound_timer = 22
                    random.choice(self.grass_sounds).play()
                animation = 'gun_run' if self.is_gun_enabled else 'run'
                self.entity.set_action(animation)
            else:
                animation = 'gun_idle' if self.is_gun_enabled else 'idle'
                self.entity.set_action(animation)
        else:
            self.air_timer += 1 * self.dt
            self.jump = True

        self.x = self.entity.x
        self.y = self.entity.y
        self.entity.change_frame(1)

        # DISPLAYS THE GUN --------------------------------------------- #
        self.entity.display(display, self.scroll)
        current_img = self.entity.get_current_img()

        if self.damage_delay >= 0:
            self.damage_delay -= dt
            current_img = pygame.mask.from_surface(current_img).to_surface()
            current_img.set_colorkey(0)

        screen.blit(current_img, (self.x - self.scroll[0], self.y - self.scroll[1]))
        if self.is_gun_enabled:
            mouse = pygame.mouse.get_pos()
            mouse = [mouse[0] // 3, mouse[1] // 3]

            angle = math.degrees(polar_angle([self.x - self.scroll[0], self.y - self.scroll[1]], mouse))
            self.gun_angle = angle
        return self.scroll, self.true_scroll
