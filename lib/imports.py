import pygame
import json


def load_image(loc, alpha=False):
    try:
        if alpha:
            return pygame.image.load(loc).convert_alpha()
        return pygame.image.load(loc).convert()
    except FileNotFoundError:
        print(f'arquivo no local {loc} nao encontrado')


def load_pallete(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    pallete = {}
    data_json = json.loads(data)
    for d in data_json['tiles']:
        image = str(d["image"]).replace("\\", "")
        pallete[str(int(d['id']) + 1)] = load_image(image, True)

    return pallete
