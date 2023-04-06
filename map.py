import pygame
import json

CHUNK_SIZE = 1
TILE_SIZE = 16
TILE_CHUNK = CHUNK_SIZE * TILE_SIZE


def load_map(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    f_map = []
    data_json = json.loads(data)
    for d in data_json['layers']:
        if d['name'] == 'Entidades':
            continue
        for i in d:
            x_axis = []
            for j in i.split(','):
                x_axis.append(j.replace('\'', ''))
            del x_axis[len(x_axis) - 1]
            f_map.append(x_axis)
    return f_map


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
    for y1 in range(round(display.get_height() / TILE_CHUNK) + 2):
        for x1 in range(round(display.get_width() / TILE_CHUNK) + 2):
            target_x = x1 - 1 + round(scroll[0] / TILE_CHUNK)
            target_y = y1 - 2 + round(scroll[1] / TILE_CHUNK)
            target_chunk = str(target_x) + ':' + str(target_y)
            if len(mapa) - 1 > target_y:
                if len(mapa[target_y]) - 1 > target_x:
                    if target_chunk not in game_map:
                        game_map[target_chunk] = generate_chunk(target_x, target_y, mapa)
                    for tile in game_map[target_chunk]:
                        if tile[1] != '0':
                            tilerect = pygame.Rect(tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE,
                                                   TILE_SIZE)
                            display.blit(tile_index[tile[1]],
                                         (tilerect.x - scroll[0], tilerect.y - scroll[1] + TILE_SIZE))
                            if tile[1] in [left_ramp, right_ramp]:
                                ramps_rects.append([tilerect, 'rampleft' if tile[1] in left_ramp else 'rampright'])
                            elif tile[1] not in ignore_list:
                                tile_rects.append(tilerect)
    return display, tile_rects, ramps_rects
