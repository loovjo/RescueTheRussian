from tile import *
from entity import Human
import math

PIXELS_PER_UNIT = 100

class World:
    def __init__(self):
        self.tiles = {} # {(x, y): Tile}
        for x in range(0, 8):
            row = []
            for y in range(0, 8):
                here = FLOOR_WOOD
                if x == 0 or x == 7 or y == 0 or y == 7:
                    here = WALL_PAPER
                self.tiles[(x, y)] = here

        self.entities = []

        self.screen_width = [0, 0]

        self.unit_origin = [0, 0]

    def draw(self, screen):
        self.screen_width = [screen.get_width(), screen.get_height()]

        self.unit_origin = self.entities[self.get_player_idx()].pos

        for (x, y), tile in self.tiles.items():
            tile.draw(screen, self, (x, y))

        for entity in self.entities:
            entity.draw(self, screen)

    def get_player_idx(self):
        for i in range(len(self.entities)):
            if isinstance(self.entities[i], Human):
                return i

    def update(self, dt):
        for entity in self.entities:
            entity.update(self, dt)

    def get_at(self, at):
        at = (int(at[0]), int(at[1]))
        if at in self.tiles:
            return self.tiles[at], at
        return VOID, at

    def transform_position(self, position):
        return [(position[0] - self.unit_origin[0]) * PIXELS_PER_UNIT + self.screen_width[0] / 2, (position[1] - self.unit_origin[1]) * PIXELS_PER_UNIT + self.screen_width[1] / 2]
