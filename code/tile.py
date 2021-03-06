from abc import ABC, abstractmethod

import math
import random
from copy import deepcopy

import pygame
from texture_asset import TextureAsset
from tile_texture import *
from entity import Shovel

class Tile(ABC):
    def __init__(self, tile_id, tile_texture):
        self.tile_texture = tile_texture
        self.tile_id = tile_id

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

        self.tile_texture.block_updated(world, at)

        height = math.ceil(bottom_right_corner[1] - top_left_corner[1])

        surf = self.tile_texture.render(height)

        screen.blit(surf, top_left_corner)

    # False = can walk through
    @abstractmethod
    def walk_on(self, entity, world, at):
        pass

    def update(self, world, at, dt):
        pass

    def __eq__(self, other):
        return isinstance(other, Tile) and self.tile_id == other.tile_id

    def copy(self):
        return deepcopy(self)

class Empty(Tile):
    def walk_on(self, entity, world, at):
        return False

class Void(Empty):
    def walk_on(self, entity, world, at):
        return False

class FloorTile(Empty):
    # Floor tiles pass on their nationality, any other type of tile blocks them
    pass

class Wall(Tile):
    def walk_on(self, entity, world, at):
        return True

BREAK_MOMENTUM_MIN = 2 * 50

class Fragile(Wall):
    def __init__(self, tile_id, break_prec, tile_texture):
        super().__init__(tile_id, tile_texture)
        self.break_prec = break_prec

    def walk_on(self, entity, world, at):
        is_above_or_below = abs(entity.pos[1] - at[1] - 0.5) > abs(entity.pos[0] - at[0] - 0.5)
        vel_to_check = entity.velocity[1] if is_above_or_below else entity.velocity[0]
        momentum_to_check = vel_to_check * entity.mass

        broke = False
        if abs(momentum_to_check) > BREAK_MOMENTUM_MIN:
            print("Bonk")

            broke = random.random() / entity.break_chance < self.break_prec

        if broke:
            world.tiles[at] = FLOOR_COBBLE()
            world.onBreakWall(at[0], at[1])
        return True

def FLOOR_WOOD():
    return FloorTile("FLOOR_WOOD", SimpleTexture(TextureAsset("floorWood.png")))

def FLOOR_COBBLE():
    return FloorTile("FLOOR_COBBLE", SimpleTexture(TextureAsset("floorCobble.png")))

def WALL_COBBLE():
    return Fragile("WALL_COBBLE", 0.1, ConnectingTexture(TextureAsset("wallCobble.png"), lambda tile_pos: (tile_pos[0] == FLOOR_WOOD() or tile_pos[0] == FLOOR_COBBLE())))

def WALL_PAPER():
    return Fragile("WALL_PAPER", 1., ConnectingTexture(TextureAsset("wallPaper.png"), lambda tile_pos: (tile_pos[0] == FLOOR_WOOD() or tile_pos[0] == FLOOR_COBBLE())))

def WALL_IRON():
    return Fragile("WALL_IRON", 0.02, ConnectingTexture(TextureAsset("wallIron.png"), lambda tile_pos: (tile_pos[0] == FLOOR_WOOD() or tile_pos[0] == FLOOR_COBBLE())))

def VOID():
    return Void("VOID", SimpleTexture(TextureAsset("empty.png")))
