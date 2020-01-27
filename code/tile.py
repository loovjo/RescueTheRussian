from abc import ABC, abstractmethod

import math
import random

import pygame
from texture_asset import TextureAsset
from tiletexture import *

class Tile(ABC):
    def __init__(self, tile_texture):
        self.tile_texture = tile_texture

    def draw(self, screen, world, at):
        top_left_corner = world.transform_position((at[0], at[1]))
        bottom_right_corner = world.transform_position((at[0] + 1, at[1] + 1))

        rect = pygame.Rect(
            *top_left_corner,
            bottom_right_corner[0] - top_left_corner[0],
            bottom_right_corner[1] - top_left_corner[1],
        )

        if not rect.colliderect(screen.get_rect()):
            return

        height = math.ceil(bottom_right_corner[1] - top_left_corner[1])

        surf = self.tile_texture.get_texture_asset(world, at).get_current_sized(height, self.tile_texture.get_render_options(world, at))

        screen.blit(surf, top_left_corner)

    # False = can walk through
    @abstractmethod
    def walk_on(self, entity, world, at):
        pass

    def update(self, world, dt):
        pass

class Empty(Tile):
    def walk_on(self, entity, world, at):
        return False

class Wall(Tile):
    def walk_on(self, entity, world, at):
        return True

BREAK_VELOCITY_MIN = 2

class Fragile(Wall):
    def __init__(self, break_prec, tile_texture):
        super().__init__(tile_texture)
        self.break_prec = break_prec

    def walk_on(self, entity, world, at):
        is_above_or_below = abs(entity.pos[1] - at[1] - 0.5) > abs(entity.pos[0] - at[0] - 0.5)
        vel_to_check = entity.velocity[1] if is_above_or_below else entity.velocity[0]

        if abs(vel_to_check) > BREAK_VELOCITY_MIN:
            print("bonk")
            if random.random() < self.break_prec:
                world.tiles[at] = FLOOR_WOOD
        return True

FLOOR_WOOD = Empty(SimpleTexture(TextureAsset(["floorWood.png"])))
WALL_COBBLE = Fragile(0.02, ConnectingTexture(TextureAsset(["wallCobble.png"]), lambda tile_pos: tile_pos[0] is FLOOR_WOOD))
WALL_PAPER = Fragile(1., ConnectingTexture(TextureAsset(["wallPaper.png"]), lambda tile_pos: tile_pos[0] is FLOOR_WOOD))
VOID = Empty(SimpleTexture(TextureAsset(["empty.png"])))
