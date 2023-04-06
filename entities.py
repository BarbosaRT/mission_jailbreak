from pygame.math import Vector2

import engine as e
import pygame
from pygame.locals import *

from atlas.rotation.main import rotate
import random
import math
pygame.init()

bullet_group = pygame.sprite.Group()


def load_image(loc, alpha=False):
    try:
        if alpha:
            return pygame.image.load(loc).convert_alpha()
        return pygame.image.load(loc).convert()
    except FileNotFoundError:
        print(f'arquivo no local {loc} nao encontrado')


def sign(value: int):
    return -1 if value < 0 else 1


def polar_angle(center, point):
    h = int(point[0] - center[0])
    v = int(point[1] - center[1])

    c_adj = math.fabs(h)
    c_oposto = math.fabs(v)

    if c_adj == 0: c_adj = 1

    # Without Angle Correction = math.atan(h / v)
    # Angle Correction
    m = sign(h) + sign(v)
    value = -360 if m == 2 else -180 if m == -2 else 0 if sign(h) == 1 else 180

    angle = math.fabs(math.radians(value) + math.atan(c_oposto / c_adj))
    return angle


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super(Bullet, self).__init__()
        angle -= 180

        self.image = pygame.Surface([2, 2])
        self.image.fill('yellow')
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=pos)
        # To apply an offset to the start position,
        # create another vector and rotate it as well.
        offset = Vector2(0, 0).rotate(-angle)

        # Use the offset to change the starting position.
        self.pos = Vector2(pos) + offset
        self.velocity = Vector2(5, 0)
        self.velocity.rotate_ip(angle)
        self.velocity.y = -self.velocity.y

    def update(self, display, scroll, enemies):
        self.rect = self.image.get_rect(center=self.pos)
        self.pos += self.velocity
        self.rect.center = self.pos
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        if self.rect.right - scroll[0] <= 0 or self.rect.bottom - scroll[1] <= 0 or \
                self.rect.top - scroll[1] >= 1360 or self.rect.left - scroll[0] >= 768:
            self.kill()
        if enemies:
            col_eny = self.collision_test(enemies, scroll)
            if col_eny:
                for enemy in col_eny:
                    enemy.attack()
                    if enemy.life == 0:
                        enemies.remove(enemy)
                    self.kill()

    def collision_test(self, rects, scroll):
        output = []
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        for rect in rects:
            if self.rect.colliderect(rect.rect):
                output.append(rect)
        return output


class Player:
    def __init__(self, x, y, tag):
        self.collision_types = {}
        self.player = e.entity(x, y, 13, 16, tag)
        self.x = x
        self.y = y
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.vertical_momentum = -5
        self.air_timer = 0
        self.grass_sound_timer = 0
        self.player_movement = [0, 0]
        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.grass_sounds = [pygame.mixer.Sound('audio/grass_0.wav'), pygame.mixer.Sound('audio/grass_1.wav')]
        self.grass_sounds[0].set_volume(0.2)
        self.grass_sounds[1].set_volume(0.2)
        self.rect = self.player.rect()
        self.gun_angle = 0
        self.scroll = [0, 0]
        self.true_scroll = [0, 0]
        self.dt = 0
        self.keys = {
            'UP': [K_w, K_UP],
            'LEFT': [K_a, K_LEFT],
            'RIGHT': [K_d, K_RIGHT],
            'CHANGE': [K_c],
            'SHOOT': [K_v]
        }
        self.guns = {
            'gun': ['images/guns/gun.png', 20],
            'shotgun': ['images/guns/shotgun.png', 5],
        }
        self.current_gun = 'gun'
        self.change_delay = 20
        self.gun_delay = self.change_delay

    def key_verifier(self, key, keys):
        for k in self.keys[key]:
            if keys[k]:
                return True
        return False

    def inputs(self):
        keys = pygame.key.get_pressed()
        if self.gun_delay > 0:
            self.gun_delay -= self.dt

        if self.key_verifier('SHOOT', keys) and self.gun_delay <= 0:
            bullet_group.add(Bullet([self.x + 6, self.y + 22], self.gun_angle + 180))
            self.gun_delay = self.change_delay

        if self.key_verifier('CHANGE', keys) and self.gun_delay <= 0:
            gk = list(self.guns.keys())
            index = gk.index(self.current_gun) + 1
            if index >= len(gk):
                index = 0
            self.current_gun = gk[index]
            self.gun_delay = self.change_delay

        # APERTOU PARA PULAR --------------------------------------------------------- #
        if self.key_verifier('UP', keys):
            if self.air_timer < 6:
                if self.vertical_momentum >= 0:
                    self.jump_sound.play()
                self.player.set_action('jump')
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

    def update(self, screen, tile_rects, ramps_rects, dt):
        self.dt = dt
        self.inputs()
        self.rect = self.player.rect()
        self.true_scroll[0] += ((self.x - self.true_scroll[0] - screen.get_width() / 2) / 20) * dt
        self.true_scroll[1] += ((self.y - self.true_scroll[1] - screen.get_height() / 2) / 20) * dt
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
        display = pygame.Surface((screen.get_width(), screen.get_height()))

        if self.grass_sound_timer > 0:
            self.grass_sound_timer -= 1

        self.player_movement = [0, 0]

        if self.dt == 0: self.dt = 1

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
            self.player.set_flip(False)

        # VERIFICA SE ESTÁ INDO PARA A ESQUERDA ------------------------------------------------------ #
        if self.player_movement[0] < 0:
            self.player.set_flip(True)

        # VERIFICA AS COLISOES ---------------------------------------------------------------------- #
        self.collision_types = self.player.move(self.player_movement, tile_rects, ramps=ramps_rects)

        # VERIFICA SE ESTA NO CHAO ------------------------------------------------------------------ #
        if self.collision_types['bottom']:
            self.jump = False
            self.air_timer = 0
            self.vertical_momentum = 0
            if self.player_movement[0] != 0:
                if self.grass_sound_timer == 0:
                    self.grass_sound_timer = 30
                    random.choice(self.grass_sounds).play()
                self.player.set_action('run')
            else:
                self.player.set_action('idle')
        else:
            self.air_timer += 1 * self.dt
            self.jump = True

        self.x = self.player.x
        self.y = self.player.y
        self.player.change_frame(1)

        # DISPLAYS THE GUN --------------------------------------------- #
        image = load_image(self.guns[self.current_gun][0])
        image.set_colorkey(0)
        image_rect = image.get_rect(topleft=(self.x, self.y + 13))
        pivot = image_rect.center

        mouse = pygame.mouse.get_pos()
        mouse = [mouse[0] // 3, mouse[1] // 3]

        image = pygame.transform.flip(image, False, mouse[0] < self.x - self.scroll[0])

        angle = math.degrees(polar_angle([self.x - self.scroll[0], self.y - self.scroll[1]], mouse))
        self.gun_angle = angle
        image_clone, image_rect_clone = rotate(pivot, image, angle, width=image.get_width() * 2, pos=[image.get_width() - 2, 0])

        self.player.display(display, self.scroll)
        screen.blit(self.player.get_current_img(), (self.x - self.scroll[0], self.y - self.scroll[1]))
        screen.blit(image_clone, (image_rect_clone.x - self.scroll[0], image_rect_clone.y - self.scroll[1]))
        return self.scroll, self.true_scroll

