from tile import GROUND, WALL
from entity import Human

PIXELS_PER_UNIT = 100

class World:
    def __init__(self):
        self.tiles = [] # [x][y]
        for x in range(0, 7):
            row = []
            for y in range(0, 7):
                here = GROUND
                if x == 0 or x == 6 or y == 0 or y == 6:
                    here = WALL
                row.append(here)
            self.tiles.append(row)

        self.entities = []

        self.screen_width = [0, 0]

        self.unit_origin = [0, 0]

    def draw(self, screen):
        self.screen_width = [screen.get_width(), screen.get_height()]

        self.unit_origin = self.entities[self.get_player_idx()].pos

        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                self.tiles[x][y].draw(screen, self, (x, y))

        for entity in self.entities:
            entity.draw(self, screen)

    def get_player_idx(self):
        for i in range(len(self.entities)):
            if isinstance(self.entities[i], Human):
                return i

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)

    def get_at(self, at):
        if 0 <= at[0] < len(self.tiles) and 0 <= at[1] < len(self.tiles[at[0]]):
            return self.tiles[at[0]][at[1]]
        return None

    def transform_position(self, position):
        return [(position[0] - self.unit_origin[0]) * PIXELS_PER_UNIT + self.screen_width[0] / 2, (position[1] - self.unit_origin[1]) * PIXELS_PER_UNIT + self.screen_width[1] / 2]
