from abc import ABC, abstractmethod

class TileTexture(ABC):
    @abstractmethod
    def get_texture_asset(self, world, at):
        pass

    @abstractmethod
    def get_rotation(self, world, at):
        pass

class SimpleTexture(TileTexture):
    def __init__(self, texture_asset):
        self.texture_asset = texture_asset

    def get_texture_asset(self, world, at):
        return self.texture_asset

    def get_rotation(self, world, at):
        return (1, )


PRIMARY_CONNECTIONS = [
    ((0, 1),   0b0001),
    ((1, 0),   0b0010),
    ((0, -1),  0b0100),
    ((-1, 0),  0b1000),
]

CORNER_CONNECTIONS = [
    ((1, 1),   0b0011),
    ((1, -1),  0b0110),
    ((-1, -1), 0b1100),
    ((-1, 1),  0b1001),
]

class ConnectingTexture(TileTexture):
    def __init__(self, texture_asset, p_connect):
        self.texture_asset = texture_asset
        self.p_connect = p_connect

    def get_texture_asset(self, world, at):
        return self.texture_asset

    def get_rotation(self, world, at):
        rotations = []
        for delta, mask in PRIMARY_CONNECTIONS:
            rat = (at[0] + delta[0], at[1] + delta[1])
            here = world.get_at(rat)
            if self.p_connect(here):
                rotations.append(mask)

        for delta, mask in CORNER_CONNECTIONS:
            rat = (at[0] + delta[0], at[1] + delta[1])
            here = world.get_at(rat)
            if self.p_connect(here):
                rotations.append(mask)

        return tuple(rotations)
