from tile import *
from collections import defaultdict
from entity import *
import math

from RescueTheRussian.code import entity
from RescueTheRussian.code.entity import *

PIXELS_PER_UNIT = 70

class World:
    def __init__(self):

        self.entities = []

        self.screen_width = [0, 0]

        self.unit_origin = [0, 0]

        self.entities.append(entity.make_player([2, 2]))

        self.tiles = defaultdict(lambda : VOID) # {(x, y): Tile}
        self.make_cellar(0, 0, "R")
        self.make_cellar(9, 2, "A")
        self.replace_area(7, 0, 1, 4, WALL_PAPER)

    def make_cellar(self, xmin, ymin, nationality):
        if nationality == "S":
            xmax = xmin + 10
            ymax = ymin + 7
        elif nationality == "A":
            xmax = xmin + 7
            ymax = ymin + 5
            self.entities.append(American([xmin + 3, ymin + 4], wa_am_front, wa_am_left, wa_am_back, wa_am_right))
            self.entities.append(American([xmin +5, ymin + 3], wa_am_front, wa_am_left, wa_am_back, wa_am_right))


        else:
            xmax = xmin + 8
            ymax = ymin + 7
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                here = None

                if x == xmin or x == xmax or y == ymin or y == ymax:
                    if self.tiles[(x, y)] == VOID:
                        here = WALL_COBBLE
                elif self.tiles[(x, y)] == VOID:
                    here = FLOOR_WOOD
                if here != None:
                    self.tiles[(x, y)] = here

    def replace_area(self, xmin, xmax, ymin, ymax, newTile):
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                self.tiles[(x, y)] = newTile

    def draw(self, screen):
        self.screen_width = [screen.get_width(), screen.get_height()]

        self.unit_origin = self.entities[0].pos

        for (x, y), tile in self.tiles.items():
            tile.draw(screen, self, (x, y))

        for entity in self.entities:
            entity.draw(self, screen)

    def get_player_idx(self):
        for i in range(len(self.entities)):
            print(i, self.entities[i])
            if isinstance(self.entities[i], Russian):
                print("hej")
                return i

    def update(self, dt):
        for entity in self.entities:
            entity.update(self, dt)

    def get_at(self, at):
        at = (int(math.floor(at[0])), int(math.floor(at[1])))
        if at in self.tiles:
            return self.tiles[at], at
        return VOID, at

    def transform_position(self, position):
        return [(position[0] - self.unit_origin[0]) * PIXELS_PER_UNIT + self.screen_width[0] / 2, (position[1] - self.unit_origin[1]) * PIXELS_PER_UNIT + self.screen_width[1] / 2]
