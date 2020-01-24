from RescueTheRussian.code import Tile

class World:
    def __init__(self):
        self.tiles = []
        for n in range (0, 50):
            row = []
            for m in range (0, 50):
                row.append(Tile)
            self.tiles.append(row)

