from tile import GROUND
from entity import Human

PIXELS_PER_UNIT = 100

class World:
    def __init__(self):
        self.tiles = [] # [x][y]
        for n in range(0, 50):
            row = []
            for m in range(0, 50):
                row.append(GROUND)
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

    def transform_position(self, position):
        return [(position[0] - self.unit_origin[0]) * PIXELS_PER_UNIT + self.screen_width[0] / 2, (position[1] - self.unit_origin[1]) * PIXELS_PER_UNIT + self.screen_width[1] / 2]
