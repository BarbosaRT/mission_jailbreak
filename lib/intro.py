import sys

import pygame

from atlas.UI import Text
from lib.background import background_3, background_2
from lib.dialogue import Dialogue
from lib.imports import load_image
from lib.intro_player import IntroPlayer
from pygame.locals import *


def make_transition(display, time_passed, surf_1, surf_2):
    background_image = display.copy()
    local_time = time_passed
    if time_passed < 0:
        local_time = -time_passed
        background_image.blit(surf_2, (0, 0))
    else:
        background_image.blit(surf_1, (0, 0))
    background_image.set_alpha(local_time)
    return background_image


def intro(screen, clock, game_size):
    player_walking_background = load_image('images/player_walking_background.png', True)
    player_caught_background = load_image('images/player_caught_background.png', True)
    player_prison_background = load_image('images/player_prison_background.png', True)

    screen_size = screen.get_size()
    height = 150

    skip_text = Text(10, 10, text="[S] skip \n[G] skip all", size=(1600, 1200),
                     font_size=50, reference=(1600, 1200), antialias=False, color=Color(50, 50, 50))

    title = Text(0, screen_size[1] / 2 - height + 50, text="", size=(1600, 1200), font_size=110,
                 reference=(1600, 1200), antialias=False, align="Center")

    title_center = Text(0, screen_size[1] / 2 - 300, text="", size=(800, 600), font_size=55,
                        reference=(800, 600), antialias=False, align="Center")

    however_text = Text(0, screen_size[1] / 2 - 300, text="However, things didn't go as planned", size=(800, 600),
                        font_size=55, reference=(800, 600), antialias=False, align="Center")

    hope_text = Text(0, screen_size[1] / 2 - 300, text="with no hope of escape.", size=(800, 600),
                     font_size=55, reference=(800, 600), antialias=False, align="Center")

    transition = Text(0, screen_size[1], text="", size=(1600, 1200), font_size=120,
                      reference=(1600, 1200), antialias=False, align="Center")
    current_dialogue = 0
    speed = 1/5
    dialogues = [
        Dialogue(title, "Alex, a skilled and highly trained spy", speed=speed),
        Dialogue(title, "Who has worked for a secret", speed=speed),
        Dialogue(title, "Intelligence agency for years, is", speed=speed),
        Dialogue(title, "now facing his toughest challenge yet...", speed=speed),
        Dialogue(transition, "............................", speed=speed, render=False),  # 4
        Dialogue(title, "His latest mission involved", speed=speed),
        Dialogue(title, "infiltrating a top-secret facility", speed=speed),
        Dialogue(title, "and stealing sensitive information", speed=speed),
        Dialogue(title, "that could compromise national security", speed=speed),
        Dialogue(transition, ".....................................", speed=speed / 2, render=False),  # 9
        Dialogue(transition, "..............", speed=speed / 2, render=False),  # 10
        Dialogue(title_center, "However, things didn't go as planned...", speed=speed),
        Dialogue(transition, "..................................", speed=speed / 2, render=False),  # 12
        Dialogue(transition, "........", speed=speed / 2, render=False),  # 12
        Dialogue(title_center, "Alex was caught", speed=speed),
        Dialogue(title_center, "Now, he finds himself imprisoned", speed=speed),
        Dialogue(title_center, "in a high-security detention center", speed=speed),
        Dialogue(title_center, "with no hope of escape...", speed=speed),
        Dialogue(transition, "......................................................", speed=speed, render=False),  # 18
        Dialogue(title, "His agency has disowned him.", speed=speed),
        Dialogue(title, "leaving him to fend for himself.", speed=speed),
        Dialogue(title, "But Alex isn't one to give up easily...", speed=speed * 0.8),
        Dialogue(transition, "......................................", speed=speed, render=False),  # 22
        Dialogue(transition, ".", render=False)
    ]
    intro_player = IntroPlayer(20, 90)

    time_passed = 255
    game_state = "Intro"

    hope_enabled = False
    however_enabled = False

    som_fundo = pygame.mixer.Sound('audio/intro.wav')
    som_fundo.play(loops=-1)
    som_fundo.set_volume(1)

    while game_state == "Intro":
        # Delta Time
        dt = 60 * (clock.tick(60) / 1000)

        game_display = pygame.Surface(game_size)
        game_display.fill("#010101")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    if current_dialogue < len(dialogues) - 2:
                        content = dialogues[current_dialogue].content
                        try:
                            current_content = len(next(dialogues[current_dialogue].gen))
                            distance = len(content) - current_content
                            for word in range(current_content, current_content + int(distance / 2)):
                                next(dialogues[current_dialogue].gen)
                        except StopIteration:
                            current_dialogue += 1
                if event.key == K_g:
                    current_dialogue = len(dialogues) - 2

        mouse = pygame.mouse.get_pos()
        scroll = [mouse[0] / 40, mouse[1] / 40]

        # Background ------------------------------------------------------------------------------------ #
        if current_dialogue < 4:
            background_3(game_display, scroll)

        elif current_dialogue == 4:
            # Transition
            time_passed -= dt * 3
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()
            background_3(background_image_1, scroll)
            background_2(background_image_2, scroll)
            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))

        elif current_dialogue <= 8:
            time_passed = 255
            background_2(game_display, scroll)
        elif current_dialogue <= 9:
            # Transition
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()
            background_2(background_image_1, scroll)

            background_2(background_image_2, scroll)
            background_image_2.blit(player_walking_background, (-scroll[0], -scroll[1]))
            intro_player.x = -time_passed * 0.4
            intro_player.update(background_image_2, scroll)
            current_img = intro_player.entity.get_current_img()
            background_image_2.blit(current_img, (intro_player.x - scroll[0], intro_player.y - scroll[1]))

            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))

        elif current_dialogue == 10:
            # Transition
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()

            background_2(background_image_1, scroll)
            background_image_1.blit(player_walking_background, (-scroll[0], -scroll[1]))
            current_img = intro_player.entity.get_current_img()
            background_image_1.blit(current_img, (intro_player.x - scroll[0], intro_player.y - scroll[1]))

            game_display.fill("#010101")

            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))
        elif current_dialogue == 11:
            time_passed = 255
            game_display.fill("#010101")
            title.write("")
        elif current_dialogue == 12:
            # Transition - ele sendo pego
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()
            background_image_1.fill("#010101")
            # however_text = True
            game_display.fill("#010101")

            background_2(background_image_2, scroll)
            background_image_2.blit(player_caught_background, (-scroll[0], -scroll[1]))

            title.write("")
            title_center.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))
        elif current_dialogue == 13:
            # Transition - ele sendo pego out
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()

            background_2(background_image_1, scroll)
            background_image_1.blit(player_caught_background, (-scroll[0], -scroll[1]))

            game_display.fill("#010101")

            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))
        elif current_dialogue < 18:
            game_display.fill("#010101")
            time_passed = 255
        elif current_dialogue == 18:
            # Transition - ele preso
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()
            background_image_1.fill("#010101")
            # hope_enabled = True
            game_display.fill("#010101")

            background_2(background_image_2, scroll)
            background_image_2.blit(player_prison_background, (-scroll[0], -scroll[1]))

            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))
        elif current_dialogue < 22:
            hope_enabled = False
            background_image_2 = game_display.copy()
            background_2(background_image_2, scroll)
            background_image_2.blit(player_prison_background, (-scroll[0], -scroll[1]))
            game_display.blit(background_image_2, (0, 0))
            time_passed = 255
        elif current_dialogue == 22:
            # Transition - ele sendo pego out
            time_passed -= dt * 2.5
            background_image_1 = game_display.copy()
            background_image_2 = game_display.copy()

            background_2(background_image_1, scroll)
            background_image_1.blit(player_prison_background, (-scroll[0], -scroll[1]))

            game_display.fill("#010101")

            title.write("")
            image = make_transition(game_display, time_passed, background_image_1, background_image_2)
            game_display.blit(image, (0, 0))
            som_fundo.fadeout(3000)
        elif current_dialogue == 23:
            game_state = "Game"

        # Front ----------------------------------------------------------------------------------------- #
        gd = pygame.transform.scale(game_display, (screen.get_width(), screen.get_height()))

        screen.blit(gd, (0, 50))

        up_surf = pygame.Surface((screen_size[0], height))
        up_surf.fill(Color(11, 11, 11))
        screen.blit(up_surf, (0, -10))
        screen.blit(up_surf, (0, screen_size[1] - height))

        # Dialogues ------------------------------------------------------------------------------------ #
        dialogues[current_dialogue].update(screen, dt)
        if dialogues[current_dialogue].done and current_dialogue < len(dialogues) - 1:
            current_dialogue += 1
            if current_dialogue in [10, 13]:
                time_passed = 255

        if hope_enabled:
            hope_text.update(screen)

        if however_enabled:
            however_text.update(screen)

        skip_text.update(screen)

        pygame.display.update()
    return game_state
