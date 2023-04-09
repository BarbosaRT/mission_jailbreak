import random
import pygame
from atlas.UI import Text


def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        # don't pause for spaces
        if letter != ' ':
            yield tmp


class Dialogue:
    def __init__(self, text: Text, content: str, speed=0.1, render=True, sound=True):
        self.done = False
        self.text = text
        self.content = content
        self.gen = text_generator(self.content)
        self.rect = pygame.Rect(0, 0, 12, 15)
        self.time_passed = 0
        self.speed = speed
        self.render = render
        self.type_sounds = [pygame.mixer.Sound('./audio/low_type.wav'),
                            pygame.mixer.Sound('./audio/medium_type.wav'),
                            pygame.mixer.Sound('./audio/high_type.wav')]
        self.type_sounds[0].set_volume(0.22)
        self.type_sounds[1].set_volume(0.22)
        self.type_sounds[2].set_volume(0.22)
        self.sound = sound
        self.delay = 5

    def update(self, display, dt):
        self.time_passed += dt * self.speed

        if self.render:
            self.text.update(display)
        if self.time_passed > 1:
            self.time_passed = 0
            try:
                if self.render and self.sound:
                    type_sound = self.type_sounds[random.randint(0, 2)]
                    type_sound.play()
                self.text.write(next(self.gen))
            except StopIteration:
                self.delay -= dt
                self.sound = False

        if self.delay <= 0:
            self.done = True
