from abc import ABC, abstractmethod

import math

import pygame
from texture_asset import TextureAsset
from tiletexture import *

class Tile(ABC):
    def __init__(self, tile_texture):
        self.tile_texture = tile_texture

    def draw(self, screen, world, at):
        top_left_corner = world.transform_position((at[0] - 0.5, at[1] - 0.5))
        bottom_right_corner = world.transform_position((at[0] + 0.5, at[1] + 0.5))

        rect = pygame.Rect(
            *top_left_corner,
            bottom_right_corner[0] - top_left_corner[0],
            bottom_right_corner[1] - top_left_corner[1],
        )

        if not rect.colliderect(screen.get_rect()):
            return

        height = math.ceil(bottom_right_corner[1] - top_left_corner[1])

        surf = self.tile_texture.get_texture_asset(world, at).get_current_sized(height, self.tile_texture.get_rotation(world, at))

        screen.blit(surf, top_left_corner)

    # False = can walk through
    @abstractmethod
    def walk_on(self, entity):
        pass

    def update(self, world, dt):
        pass

class Empty(Tile):
    def walk_on(self, entity):
        return False

class Wall(Tile):
    def walk_on(self, entity):
        return True

GROUND = Empty(SimpleTexture(TextureAsset(["floorWood.png"])))
WALL = Wall(ConnectingTexture(TextureAsset(["wallCobble.png"]), lambda tile: isinstance(tile, Empty)))
