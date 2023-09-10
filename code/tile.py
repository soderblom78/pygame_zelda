import pygame
from settings import *
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_name):
        super().__init__(groups)
        self.sprite_type = tile_name
        self.image = pygame.image.load(f"../graphics/test/{self.sprite_type}.png").convert_alpha()
        if self.sprite_type == "tree":
            self.rect = self.image.get_rect(topleft=(pos[0], (pos[1] - TILESIZE * 1.5)))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, -10)




