import pygame
import json

from atlas.lighting.Ray import Ray
from lib.camera import Camera
from lib.checkpoint import Checkpoint
from lib.guard import Guard
from lib.imports import load_pallete
from lib.frog import Frog
from lib.pickup_gun import PickupGun

CHUNK_SIZE = 1
TILE_SIZE = 16
TILE_CHUNK = CHUNK_SIZE * TILE_SIZE

pallete = load_pallete('./paleta.tsj')


def get_entities(d):
    f_entities = []
    for y in range(0, d['height']):
        for j in range(0, d['width']):
            value = d['data'][j + y * d['width']]
            if value == 4:
                # Down laser
                f_entities.append(Camera(pos=(j * TILE_SIZE, (y + 1.5) * TILE_SIZE)))
            if value == 22:
                # left blinking laser
                f_entities.append(Camera(pos=(j * TILE_SIZE, (y + 1.5) * TILE_SIZE),
                                         start_angle=270, fov=0, blink=True))
            if value == 23:
                # down moving laser
                f_entities.append(Camera(pos=(j * TILE_SIZE, (y + 1.5) * TILE_SIZE),
                                         fov=0, move=True))
            if value == 24:
                # Elevator 1
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=(j * TILE_SIZE, (y - 18) * TILE_SIZE)))
            if value == 25:
                # Elevator 2
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=(j * TILE_SIZE, (y - 18) * TILE_SIZE)))
            if value == 26:
                # Elevator 3
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=(j * TILE_SIZE, (y - 18) * TILE_SIZE)))
            if value == 27:
                # Elevator 4
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=(j * TILE_SIZE, (y - 18) * TILE_SIZE)))
            if value == 28:
                # Elevator 5
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=(j * TILE_SIZE, (y - 18) * TILE_SIZE)))
            if value == 29:
                # Normal Elevator
                f_entities.append(Checkpoint(pos=(j * TILE_SIZE, (y + 2) * TILE_SIZE), image=pallete[str(value)],
                                             dest=None))
            if value == 30:
                # Up blinking laser
                f_entities.append(Camera(pos=((j + 0.5) * TILE_SIZE, (y + 0.75) * TILE_SIZE),
                                         start_angle=180, fov=0, blink=True))
            if value == 31:
                # Up laser
                f_entities.append(Camera(pos=((j + 0.5) * TILE_SIZE, (y + 0.75) * TILE_SIZE),
                                         start_angle=180))
            if value == 32:
                f_entities.append(Frog(x=j * TILE_SIZE, y=y * TILE_SIZE))

            if value == 33:
                f_entities.append(PickupGun(pos=(j * TILE_SIZE, y * TILE_SIZE)))
            if value == 34:
                f_entities.append(Guard(x=j * TILE_SIZE, y=(y - 0.5) * TILE_SIZE))
            if value == 52:
                f_entities.append(Ray(origin=(j * TILE_SIZE, (y + 1) * TILE_SIZE)))

    return f_entities


def load_map(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    f_map = []
    f_entities = []
    f_fundo = []
    data_json = json.loads(data)
    for d in data_json['layers']:
        if d['name'] == 'Entidades':
            f_entities = get_entities(d)
            continue
        if d['name'] == 'Fundo':
            for y in range(0, d['height']):
                x_axis = []
                for j in range(0, d['width']):
                    block = d['data'][j + y * d['width']]
                    x_axis.append(str(block))
                f_fundo.append(x_axis)
            continue
        for y in range(0, d['height']):
            x_axis = []
            for j in range(0, d['width']):
                block = d['data'][j + y * d['width']]
                x_axis.append(str(block))
            f_map.append(x_axis)

    return f_map, f_entities, f_fundo


# Tile_index example
# final_index = {'1': load_image('dungeon/tiles/tile_1.png'),
#                '2': load_image('dungeon/tiles/tile_2.png'),


def generate_chunk(x, y, mapa):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x1 = x * CHUNK_SIZE + x_pos
            target_y1 = y * CHUNK_SIZE + y_pos
            if target_x1 >= 0 and len(mapa) > target_y1 >= 0:
                f = mapa[target_y1]
                if len(f) > target_x1:
                    tile_type = f[target_x1]
                else:
                    tile_type = '0'
            else:
                tile_type = '0'
            chunk_data.append([[target_x1, target_y1], tile_type])
    return chunk_data


def show_map(screen: pygame.Surface, mapa, tile_index, scroll, left_ramp='', right_ramp='', ignore_list=()):
    display = pygame.Surface((screen.get_width(), screen.get_height()))
    display.set_colorkey(0)
    game_map = {}
    tile_rects = []
    ramps_rects = []
    respawn_rects = []
    final_rects = []

    mask_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    mask_surface.set_colorkey('#000000')

    for y1 in range(round(display.get_height() / TILE_CHUNK) + 3):
        for x1 in range(round(display.get_width() / TILE_CHUNK) + 2):
            target_x = x1 - 1 + round(scroll[0] / TILE_CHUNK)
            target_y = y1 - 2 + round(scroll[1] / TILE_CHUNK)
            target_chunk = str(target_x) + ':' + str(target_y)
            if len(mapa) > abs(target_y):
                if len(mapa[target_y]) - 1 > target_x:
                    if target_chunk not in game_map:
                        game_map[target_chunk] = generate_chunk(target_x, target_y, mapa)
                    for tile in game_map[target_chunk]:
                        if tile[1] == '41':
                            tilerect = pygame.Rect(tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE,
                                                   TILE_SIZE)
                            respawn_rects.append(tilerect)
                            continue
                        if tile[1] == '44':
                            tilerect = pygame.Rect(tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE,
                                                   TILE_SIZE)
                            final_rects.append(tilerect)
                            continue
                        if tile[1] != '0':
                            tilerect = pygame.Rect(tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE,
                                                   TILE_SIZE)

                            # Creates the masks --------------------------------------------- #
                            position = (tilerect.x - scroll[0], tilerect.y - scroll[1] + TILE_SIZE)
                            mask_surf = pygame.mask.from_surface(tile_index[tile[1]]).to_surface()
                            mask_surf.set_colorkey('#000000')
                            mask_surface.blit(mask_surf, position)

                            display.blit(tile_index[tile[1]], position)
                            if tile[1] in [left_ramp, right_ramp]:
                                ramps_rects.append([tilerect, 'rampleft' if tile[1] in left_ramp else 'rampright'])
                            elif tile[1] not in ignore_list:
                                tile_rects.append(tilerect)
    return display, tile_rects, ramps_rects, mask_surface, respawn_rects, final_rects


def show_fundo(screen: pygame.Surface, mapa, tile_index, scroll):
    display = pygame.Surface((screen.get_width(), screen.get_height()))
    display.set_colorkey(0)
    game_map = {}

    for y1 in range(round(display.get_height() / TILE_CHUNK) + 3):
        for x1 in range(round(display.get_width() / TILE_CHUNK) + 3):
            target_x = x1 - 2 + round(scroll[0] / TILE_CHUNK)
            target_y = y1 - 2 + round(scroll[1] / TILE_CHUNK)
            target_chunk = str(target_x) + ':' + str(target_y)
            if len(mapa) > abs(target_y):
                if len(mapa[target_y]) - 1 > target_x:
                    if target_chunk not in game_map:
                        game_map[target_chunk] = generate_chunk(target_x, target_y, mapa)
                    for tile in game_map[target_chunk]:
                        if tile[1] != '0':
                            tilerect = pygame.Rect(tile[0][0] * TILE_SIZE, (tile[0][1] - 1) * TILE_SIZE, TILE_SIZE,
                                                   TILE_SIZE)
                            position = (tilerect.x - scroll[0], tilerect.y - scroll[1] + TILE_SIZE)

                            display.blit(tile_index[tile[1]], position)
    return display
