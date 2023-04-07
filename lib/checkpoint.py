class Checkpoint:
    def __init__(self, pos, image, dest):
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(bottomleft=pos)
        self.dest = dest

    def update(self, display, scroll, player):
        local_pos = (self.rect.x - scroll[0], self.rect.y - scroll[1])
        local_rect = self.image.get_rect(topleft=local_pos)

        local_player_rect = player.rect.copy()
        local_player_rect.x -= scroll[0]
        local_player_rect.y -= scroll[1] - 16

        if local_player_rect.colliderect(local_rect) and self.dest is not None:
            player.entity.set_pos(self.dest[0], self.dest[1])

        display.blit(self.image, local_pos)
