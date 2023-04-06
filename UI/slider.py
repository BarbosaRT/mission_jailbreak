import pygame
from UI.essentials import create_surf


class Slider:
    def __init__(self, x, y, handle_size=30, handle_color=pygame.Color(255, 255, 255, 255), length=100,
                 back_color=pygame.Color(100, 100, 100, 255), fill_color=pygame.Color(200, 200, 200, 10),
                 horizontal=True, invert=False, reference=(1280, 720), height=20):
        """
        :summary: A Slider object that returns a value depending on the position of the handle

        :param x: x position of the slider
        :param y: y position of the slider
        :param handle_size: size of the handle
        :param handle_color: set the handle color
        :param length: length of the slider
        :param back_color: set the back color
        :param fill_color: set the fill color
        :param horizontal: with the slider will be horizontal oriented
        :param invert: changes the start position of the fill from left to right or top to bottom
        :param reference: use a reference resolution to scale the ui
        :param height: height of the slider
        """

        self.x = x
        self.y = y

        self.handle_color = handle_color
        self.back_color = back_color
        self.fill_color = fill_color

        self.length = length
        self.original_length = length
        self.hx = self.x - (handle_size - height) / 2 if not horizontal else self.x + length if invert else self.x
        self.hy = self.y - (handle_size - height) / 2 if horizontal else self.y if not invert else self.y + length
        self.handle_Rect = pygame.Rect(self.hx, self.hy, handle_size + 10, handle_size + 10)
        # position and rect of the handle
        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.value = 0
        self.horizontal = horizontal
        self.height = height
        self.inverted = invert
        self.handle_size = handle_size
        self.handle = pygame.Surface((0, 0))
        self.use_fill = True
        self.fill_value = 0
        self.reference = reference
        self.scale = (0, 0)
        self.fill_right = self.value
        self.screen_size = (0, 0)

    def handle_movement(self):
        mouse_pos = pygame.mouse.get_pos()  # Get the mouse position

        # Rescale the length of the handle
        self.length = int(self.original_length * (self.scale[0] if self.horizontal else self.scale[1]))

        # Rescale the rect of the handle
        self.handle_Rect.size = ((self.handle_size + 10 * self.scale[0]) * self.scale[0],
                                 (self.handle_size + 10 * self.scale[1]) * self.scale[1])

        # Verify with the mouse is colliding with the handle
        if self.handle_Rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            # Verify with the mouse clicked while is colliding with the handle
            clicked = pygame.mouse.get_pressed(3)[0]
            if clicked:
                if self.horizontal:
                    self.handle_Rect.x = mouse_pos[0] - self.handle_size / 2
                    self.fill_value = self.handle_Rect.x + self.handle_size / 2 - self.x
                    self.value = round(((self.fill_value - self.handle_size * (
                        self.scale[0] if self.horizontal else self.scale[1])) / self.length) * 100) / 100
                else:
                    self.handle_Rect.y = mouse_pos[1] - self.handle_size / 2
                    self.fill_value = self.handle_Rect.y + self.handle_size / 2 - self.y

        # Set Limits for the handle
        if self.horizontal:
            if self.x > self.handle_Rect.x:  # LEFT Limit
                self.handle_Rect.x -= self.handle_Rect.x - self.x

            elif self.handle_Rect.x > self.x + self.length:  # RIGHT Limit
                self.handle_Rect.x -= self.handle_Rect.x - (self.x + self.length)
        else:
            if self.y > self.handle_Rect.y:  # TOP Limit
                self.handle_Rect.y -= self.handle_Rect.y - self.y

            elif self.handle_Rect.y > self.y + self.length:  # BOTTOM Limit
                self.handle_Rect.y -= self.handle_Rect.y - (self.y + self.length)

    def change_position(self, x, y):
        if x == self.x and y == self.y:
            return
        self.x = x
        self.y = y

        # Rescale the length of the handle
        self.length = int(self.original_length * (self.scale[0] if self.horizontal else self.scale[1]))

        self.handle_Rect.x = 0
        self.handle_Rect.y = 0

        # Set Limits for the handle
        if self.x > self.handle_Rect.x:  # LEFT Limit
            self.handle_Rect.x -= self.handle_Rect.x - self.x

        elif self.handle_Rect.x > self.x + self.length:  # RIGHT Limit
            self.handle_Rect.x -= self.handle_Rect.x - (self.x + self.length)

        if self.y > self.handle_Rect.y:  # TOP Limit
            self.handle_Rect.y -= self.handle_Rect.y - self.y

        elif self.handle_Rect.y > self.y + self.length:  # BOTTOM Limit
            self.handle_Rect.y -= self.handle_Rect.y - (self.y + self.length)

        # Handle Centering
        if self.horizontal:
            self.handle_Rect.y -= self.handle_size / 6
            self.handle_Rect.x += self.value * self.length + self.handle_size / 2 * self.scale[0] * (
                -1 if self.inverted else 1)
        else:
            self.handle_Rect.x -= self.handle_size / 6
            self.handle_Rect.y += self.value * self.length + self.handle_size / 2 * self.scale[1] * (
                -1 if self.inverted else 1)

    def update(self, display: pygame.Surface):
        # HANDLE
        self.scale = (round(display.get_width() / self.reference[0], 2),
                      round(display.get_height() / self.reference[1], 2))
        handle = create_surf(self.handle_size * self.scale[0], self.handle_size * self.scale[1],
                             self.handle_color)  # Handle's Surface
        self.handle = handle
        self.handle_movement()

        # BACK
        back_x = self.length + handle.get_width() if self.horizontal else self.height * self.scale[0]
        back_y = self.length + handle.get_height() if not self.horizontal else self.height * self.scale[1]
        back = create_surf(back_x, back_y, self.back_color)  # Back's Surface

        back_rect = back.get_rect(topleft=[self.x, self.y])  # Back's Rect
        self.back_rect = back_rect

        # Fill the back
        if self.horizontal:
            fill_rect = pygame.Rect(0, 0, self.value * self.length + self.handle_size * self.scale[0],
                                    self.height * self.scale[1])
            fill_rect.right = back_rect.right - self.x if self.inverted else fill_rect.right
        else:
            fill_rect = pygame.Rect(0, 0, self.height * self.scale[0],
                                    self.value * self.length + self.handle_size * self.scale[1])
            fill_rect.bottom = back_rect.bottom - self.y if self.inverted else fill_rect.bottom
        self.fill_right = fill_rect.right

        back.fill(self.fill_color, fill_rect)

        # ADJUSTICES THE HANDLE ON SCREEN WHEN RESIZING
        if self.screen_size != display.get_size():
            if self.horizontal:
                self.handle_Rect.x = round(self.x + self.value * self.length)
            else:
                self.handle_Rect.y = round(self.y + self.value * self.length)
        # DISPLAY
        display.blit(back, back_rect)
        display.blit(handle, self.handle_Rect)
        self.screen_size = display.get_size()
