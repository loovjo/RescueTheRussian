from tile import GROUND

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

    def draw(self, screen):
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                self.tiles[x][y].draw(screen, self, (x, y))

        for entity in self.entities:
            entity.draw(self, screen)

        self.screen_width = [screen.get_width(), screen.get_height()]

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)

    def transform_position(self, position):
        return [position[0] * PIXELS_PER_UNIT + self.screen_width[0] / 2, position[1] * PIXELS_PER_UNIT + self.screen_width[1] / 2]
