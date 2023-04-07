import json

import pygame
import sys
from pygame.locals import *

from atlas.lighting.Ray import Ray
from imports import load_pallete
from lib.camera import Camera
from lib.checkpoint import Checkpoint
from lib.frog import Frog
# from UI import *
from map import show_map, load_map
from entities import Player, bullet_group
import engine as e
import time

# PyGame Info ------------------------------------------------------ #
WINDOWSIZE = (800, 600)
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Template')
GAME_SIZE = (WINDOWSIZE[0]/3, WINDOWSIZE[1]/3)
game_display = pygame.Surface(GAME_SIZE)
screen = pygame.display.set_mode(WINDOWSIZE, RESIZABLE)


# Music -------------------------------- #
# som_fundo = pygame.mixer.Sound('audio/music.mp3')
# som_fundo.play(loops=-1)


# Animations --------------------------- #
e.load_animations('images/entities/')

# Map ------------------------ #
mapa, entidades = load_map('teste.json')
tile_index = load_pallete('paleta.tsj')
scroll = [46, 1500]

# Delta Time -------------- #
dt = time.time()
last_time = time.time()

# Colors -------------------- #
ORANGE = pygame.Color(205, 75, 0)

# Entities --------------------- #
player = Player(180, 800, 'player')
tile_rects = []
ramps_rects = []


def update_entities(display_surface, mask_surface):
    global player
    for entidade in entidades:
        if type(entidade) == Camera:
            entidade.update(display_surface, scroll, dt, mask_surface, player.rect)
        if type(entidade) == Checkpoint:
            entidade.update(display_surface, scroll, player)
        if type(entidade) == Frog:
            entidade.update(display_surface, scroll, dt, tile_rects, ramps_rects)


def main():
    global dt, scroll, last_time, game_display, player, tile_rects, ramps_rects
    mask = pygame.Surface(GAME_SIZE)
    mask.fill((100, 100, 100, 1))

    bulb = Ray((400, 100), 90, 45, ORANGE, GAME_SIZE)

    while 1:
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

        # Level ----------------------------------------------------------------------------------------- #
        map_display, tile_rects, ramps_rects, mask_surface = show_map(game_display, mapa, tile_index, scroll,
                                                                      left_ramp='17', right_ramp='16')
        game_display.blit(map_display, (0, 0))
        game_display.blit(mask, (0, 0), special_flags=BLEND_RGBA_MULT)

        # Bullets ----------------------------------------------------------------------------------------------- #
        bullet_group.update(display=game_display, scroll=scroll, enemies=[])

        # Entidades ------------------------------------------------------------------------------------- #
        update_entities(game_display, mask_surface)

        # Player ---------------------------------------------------------------------------------------- #
        scroll, true_scroll = player.update(game_display, tile_rects, ramps_rects, dt)
        # game_display.blit(player.player.get_current_img(), (player.x - scroll[0], player.y - scroll[1]))

        # Light ----------------------------------------------------------------------------------------- #
        bulb.render(game_display, mask_surface)

        gd = pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()))
        screen.blit(gd, (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    main()
