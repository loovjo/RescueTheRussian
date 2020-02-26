from tile import *
from collections import defaultdict
from entity import *
import math
from queue import PriorityQueue
from random import random, choice

PIXELS_PER_UNIT = 70

def ifloor(x):
    return int(math.floor(x))

def iceil(x):
    return int(math.ceil(x))

class World:
    def __init__(self):

        self.entities = []

        self.screen_width = [0, 0]

        self.unit_origin = [0, 0]

        self.entities.append(make_player([2, 2]))
        self.entities.append(make_swede([3, 2]))
        self.entities.append(make_flag_am([5, 1.25]))
        self.entities.append(make_flag_sw([7, 1.25]))
        self.entities.append(make_flag_ru([3, 1.25]))
        self.entities.append(make_crucible([3, 3.25]))

        self.tiles = defaultdict(lambda: VOID())  # {(x, y): Tile}
        self.make_cellar(0, 0, 0, 0, "R")
        self.make_cellar(8, 0, 2, 0, "A")
        self.replace_area(8, 8, 3, 4, WALL_PAPER())

        self.tile_nationality = {}  # {pos: (nationality, distance to flag)}

        self.update_tile_nationality((2, 2), 'rus')
        print(self.tile_nationality)

    def draw(self, screen):
        self.screen_width = [screen.get_width(), screen.get_height()]

        self.unit_origin = self.entities[0].pos

        for (x, y), tile in self.tiles.items():
            tile.draw(screen, self, (x, y))

        for entity in self.entities:
            entity.draw(self, screen)

    def get_at(self, at):
        at = (int(math.floor(at[0])), int(math.floor(at[1])))
        if at in self.tiles:
            return self.tiles[at], at
        return VOID(), at

    def get_player_idx(self):
        for i in range(len(self.entities)):
            if isinstance(self.entities[i], Russian):
                return i

    def make_cellar(self, xmin, xsize, ymin, ysize, nationality):
        if nationality == "S":
            if xsize == 0:
                xsize = 10
            if ysize == 0:
                ysize = 7
        elif nationality == "A":
            if xsize == 0:
                xsize = 7
            if ysize == 0:
                ysize = 5
            self.entities.append(
                make_american([xmin + 1 + math.floor(random() * (xsize-1)), ymin + 1 + math.floor(random() * (ysize-1))]))
        else:
            if xsize == 0:
                xsize = 8
            if ysize == 0:
                ysize = 7

        xmax = xmin + xsize
        ymax = ymin + ysize

        wall_type = choice([WALL_COBBLE, WALL_IRON])

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                here = None

                if x == xmin or x == xmax or y == ymin or y == ymax:
                    if self.tiles[(x, y)] == VOID():
                        here = wall_type()
                elif self.tiles[(x, y)] == VOID():
                    here = FLOOR_WOOD()
                if here is not None:
                    self.tiles[(x, y)] = here

    def onBreakWall(self, tile_x, tile_y):

        # add rock piece
        rock = make_rock([0, 0])
        rock.pos[0] = tile_x + rock.width / 2 + random() * (1 - rock.width)
        rock.pos[1] = tile_y + rock.height / 2 + random() * (1 - rock.height)
        self.entities.append(rock)

        # add new room
        if random() < 0.2:
            sizex = 7 + math.floor((random()-0.5)*2)
            sizey = 5 + math.floor((random()-0.5)*2)
            locations = [[]]
            for x in range(tile_x - sizex, tile_x + 1):
                for y in range(tile_y - sizey, tile_y + 1):
                    if (x == tile_x - sizex or x == tile_x) and (y == tile_y - sizey or y == tile_y):
                        continue
                    if self.is_void(x + 1, x + sizex - 1, y + 1, y + sizey - 1):
                        locations.append([x, y])
            pos = locations[math.floor(random() * (len(locations)))]
            if len(pos) == 2:
                self.make_cellar(pos[0], sizex, pos[1], sizey, "A")

        # fill up gaps in wall with cobble
        for x in range(tile_x - 1, tile_x + 2):
            for y in range(tile_y - 1, tile_y + 2):
                if self.tiles[(x, y)] == VOID():
                    self.tiles[(x, y)] = WALL_COBBLE()

    def is_void(self, xmin, xmax, ymin, ymax):
        empty = True
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                if self.tiles[(x, y)] != VOID():
                    empty = False
                    break
            if not empty:
                break
        return empty

    def replace_area(self, xmin, xmax, ymin, ymax, newTile):
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                self.tiles[(x, y)] = newTile.copy()

    def transform_position(self, position):
        return [(position[0] - self.unit_origin[0]) * PIXELS_PER_UNIT + self.screen_width[0] / 2,
                (position[1] - self.unit_origin[1]) * PIXELS_PER_UNIT + self.screen_width[1] / 2]

    def update(self, dt):
        # Map from integer coordinates to list of indicies into self.entities
        tile_entidx_map = defaultdict(list)
        # Map from entity index to coordinate list
        entidx_tile_map = defaultdict(list)
        for i, entity in enumerate(self.entities):
            top_left_corner = (ifloor(entity.pos[0] - entity.width), ifloor(entity.pos[1] - entity.height))
            bottom_right_corner = (iceil(entity.pos[0] - entity.width), iceil(entity.pos[1] - entity.height))
            for x in range(top_left_corner[0], bottom_right_corner[0] + 1):
                for y in range(top_left_corner[1], bottom_right_corner[1] + 1):
                    tile_entidx_map[(x, y)].append(i)
                    entidx_tile_map[i].append((x, y))

        for i, entity in enumerate(self.entities):
            collision_idxs = set()
            for ipos in entidx_tile_map[i]:
                collision_idxs |= set(tile_entidx_map[ipos])

            entity.update(self, dt, collision_idxs)

        for (at, tile) in self.tiles.items():
            tile.update(self, at, dt)

    def update_tile_nationality(self, pos, nationality):
        visited = set()
        visiting = PriorityQueue()  # Contains (-distance, (x, y))
        visiting.put((0, pos))

        while not visiting.empty():
            ndist, (x, y) = visiting.get()
            distance = -ndist
            if (x, y) in visited:
                continue

            visited.add((x, y))

            tile, _ = self.get_at((x, y))
            if not isinstance(tile, FloorTile):
                continue

            if (x, y) in self.tile_nationality:
                _, prev_distance = self.tile_nationality[(x, y)]
                if prev_distance <= distance:
                    continue

            self.tile_nationality[(x, y)] = (nationality, distance)
            for dx, dy in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
                rx, ry = x + dx, y + dy
                visit = (-(distance + 1), (rx, ry))
                visiting.put(visit)

    def remove_entity(self, entity):
        self.entities.remove(entity)
