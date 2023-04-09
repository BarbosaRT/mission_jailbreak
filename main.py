import math

import pygame
import sys
from pygame.locals import *

from atlas.lighting import Ray
from atlas.lighting.bulb import Bulb
from lib.dialogue import Dialogue

# PyGame Info ------------------------------------------------------ #
WINDOWSIZE = (800, 600)
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Mission Jailbreak')
GAME_SIZE = (WINDOWSIZE[0]/2.5, WINDOWSIZE[1]/2.5)
game_display = pygame.Surface(GAME_SIZE)
screen = pygame.display.set_mode(WINDOWSIZE)

from atlas.UI import Text
from lib.background import background, background_2
from lib.imports import load_pallete, load_image
from lib.camera import Camera
from lib.checkpoint import Checkpoint
from lib.frog import Frog
from lib.guard import Guard
from lib.intro import intro

from lib.map import show_map, load_map, show_fundo
from lib.entities import bullet_group
from lib.player import Player
import engine as e
import time

from lib.pickup_gun import PickupGun

# Animations --------------------------- #
icon = load_image('images/icon.png', True)
pygame.display.set_icon(icon)
e.load_animations('images/entities/')

# Map ------------------------ #
mapa, entidades, fundo = load_map('teste.json')
tile_index = load_pallete('paleta.tsj')
scroll = [700, 3200]

# Delta Time -------------- #
dt = time.time()
last_time = time.time()

# Colors -------------------- #
ORANGE = pygame.Color(205, 75, 0)

# Entities --------------------- #
# 700, 3200
checkpoint_pos = [700, 3200]

player = Player(checkpoint_pos[0], checkpoint_pos[1], 'player')
player.checkpoint_pos = checkpoint_pos
tile_rects = []
ramps_rects = []
respawn_rects = []

# Game State ----------------------------- #
game_state = "Menu"

# Music -------------------------------- #
som_fundo = pygame.mixer.Sound('audio/menu.mp3')
som_fundo.play(loops=-1)
som_fundo.set_volume(0)


def update_entities(display_surface, mask_surface):
    global player
    enemies = []
    for entidade in entidades:
        if type(entidade) == Bulb:
            entidade.update(display_surface, scroll, mask_surface)
        if type(entidade) == Ray:
            entidade.update(display_surface, scroll, mask_surface)

        if type(entidade) == Camera:
            player_mask = pygame.mask.from_surface(player.entity.get_current_img()).to_surface()
            player_mask.set_colorkey('#000000')
            player_pos = [player.rect.x - scroll[0], player.rect.y - scroll[1]]
            mask_surface.blit(player_mask, player_pos)
            entidade.update(display_surface, scroll, dt, mask_surface, player)
            continue

        if type(entidade) == Checkpoint:
            entidade.update(display_surface, scroll, player)
            continue
        if type(entidade) == Frog:
            enemies.append(entidade)
            entidade.update(display_surface, scroll, dt, tile_rects, ramps_rects, player)
            continue
        if type(entidade) == PickupGun:
            entidade.update(display_surface, scroll, dt, player)
            continue
        if type(entidade) == Guard:
            enemies.append(entidade)
            entidade.update(display_surface, scroll, player)
            continue
    return enemies


def game_loop():
    global dt, scroll, last_time, game_display, player, tile_rects, ramps_rects, som_fundo, respawn_rects
    is_fadein = True
    has_faded_music = False
    time_passed = 0

    mask = pygame.Surface(GAME_SIZE)
    mask.fill((0, 0, 0, 255))

    som_fundo = pygame.mixer.Sound('audio/background_music.mp3')
    som_fundo.play(loops=-1)
    som_fundo.set_volume(0)

    screen_size = screen.get_size()
    life_text = Text(10, 10, text="Life: 1\n[R] respawn", size=(1600, 1200),
                     font_size=50, reference=(1600, 1200), antialias=False, color=Color(100, 100, 100))

    final_text = Text(0, screen_size[1] / 2 - 300, text="", size=(800, 600),
                      font_size=55, reference=(800, 600), antialias=False, align="Center")

    final_dialogue = Dialogue(final_text, "Mission Complete", speed=1/20)
    dialogue_enabled = False

    while game_state == "Game":
        # Delta Time
        dt = 60 * (clock.tick(60) / 1000)
        last_time = time.time()

        game_display = pygame.Surface(GAME_SIZE)
        game_display.fill("#222222")
        game_display.set_colorkey(0)

        screen.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Background ------------------------------------------------------------------------------------ #
        background_2(game_display, scroll)

        # Fundo ---------------------------------------------------------------------------------------- #
        fundo_display = show_fundo(game_display, fundo, tile_index, scroll)
        game_display.blit(fundo_display, (0, 0))

        # Level ----------------------------------------------------------------------------------------- #
        map_display, tile_rects, ramps_rects, \
        mask_surface, respawn_rects, final_rects = show_map(game_display, mapa, tile_index, scroll,
                                                            left_ramp='17', right_ramp='16')
        game_display.blit(map_display, (0, 0))
        # game_display.blit(mask, (0, 0), special_flags=BLEND_RGBA_MULT)

        # Entidades ------------------------------------------------------------------------------------- #
        enemies = update_entities(game_display, mask_surface)
        enemies.append(player)

        # Bullets ----------------------------------------------------------------------------------------------- #
        bullet_group.update(display=game_display, scroll=scroll, enemies=enemies,
                            tile_rects=tile_rects, ramps_rects=ramps_rects)

        # Player ---------------------------------------------------------------------------------------- #
        if player.life <= 0 or (player.final and not is_fadein):
            time_passed = 4
            is_fadein = True
            if not player.final:
                mask.set_alpha(255)
        scroll, true_scroll = player.update(game_display, tile_rects, ramps_rects, dt,
                                            respawn_rects, final_rects)
        life_text.write(f'[R] respawn\nLife: {player.life}')
        # game_display.blit(player.player.get_current_img(), (player.x - scroll[0], player.y - scroll[1]))

        # Transition ------------------------------------------------------------------------------------ #
        time_passed += dt / 5
        v = (time_passed - 10) * 5
        if player.final and is_fadein:
            dialogue_enabled = v >= 280
            mask.set_alpha(v)
            player.entity.set_action('run')
        elif is_fadein and time_passed > 10:
            value = (time_passed - 10) * (time_passed - 10) * 2
            if 255 - value > 0:
                mask.set_alpha(255 - value)
                if not has_faded_music:
                    som_fundo.set_volume(value / 255)
            else:
                is_fadein = False
                has_faded_music = True
        game_display.blit(mask, (0, 0), special_flags=BLEND_ALPHA_SDL2)


        # Display --------------------------------------------------------------------------------------- #
        gd = pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()))
        screen.blit(gd, (0, 0))

        # Front ----------------------------------------------------------------------------------------- #
        height = 80
        up_surf = pygame.Surface((screen_size[0], height))
        up_surf.fill(Color(11, 11, 11))
        screen.blit(up_surf, (0, -10))
        screen.blit(up_surf, (0, screen_size[1] - height))

        # UI ---------------------------------------------------------------------------------------------- #
        life_text.update(screen)
        if dialogue_enabled:
            dialogue_surf = pygame.Surface(WINDOWSIZE)
            dialogue_surf.set_colorkey(0)
            final_dialogue.update(dialogue_surf, dt)
            dialogue_surf.set_alpha((v - 260) * 2)
            som_fundo.fadeout(3000)
            screen.blit(dialogue_surf, (0, 0))

        pygame.display.update()


def ui_screen():
    global game_display, scroll, game_state, dt
    screen_size = screen.get_size()
    title_start_y = screen_size[1] / 2 - 60
    title = Text(10, title_start_y, text="Mission: Jailbreak ", size=(700, 200), font_size=100,
                 reference=(800, 600), antialias=True)

    press_start_y = screen_size[1] / 2 + 10
    press = Text(11, press_start_y, text="Press R to start ", size=(700, 200), font_size=50,
                 reference=(800, 600), antialias=True)
    is_fadein = True
    time_passed = 0
    som_fundo.set_volume(0)
    while game_state == "Menu":
        # Delta Time
        dt = 60 * (clock.tick(60) / 1000)
        time_passed += dt / 120

        if time_passed >= math.pi:
            time_passed = 0

        if is_fadein:
            som_fundo.set_volume(time_passed)
            if time_passed >= 1:
                is_fadein = False

        game_display = pygame.Surface(GAME_SIZE)
        game_display.fill("#222222")
        game_display.set_colorkey(0)

        screen.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    game_state = "Intro"
                    som_fundo.fadeout(2000)

        mouse = pygame.mouse.get_pos()
        scroll = [mouse[0] / 40, mouse[1] / 40]

        # Background ------------------------------------------------------------------------------------ #
        background(game_display, scroll, enable_vertical=False)

        # Display --------------------------------------------------------------------------------------- #
        gd = pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()))
        screen.blit(gd, (0, 0))

        # Front ----------------------------------------------------------------------------------------- #
        height = 100
        screen_size = screen.get_size()
        up_surf = pygame.Surface((screen_size[0], height))
        up_surf.fill(Color(11, 11, 11))
        screen.blit(up_surf, (0, -10))
        screen.blit(up_surf, (0, screen_size[1] - height))

        # UI -------------------------------------------------------------------------------------------- #
        title.update(screen)
        title.y = title_start_y + math.sin(time_passed * 5) * 2

        press.update(screen)
        press.y = press_start_y + math.sin(time_passed * 5) * 2

        pygame.display.update()


def main():
    global game_state
    while 1:
        if game_state == "Menu":
            ui_screen()
        elif game_state == "Intro":
            game_state = intro(screen, clock, GAME_SIZE)
        elif game_state == "Game":
            game_loop()


if __name__ == '__main__':
    main()
