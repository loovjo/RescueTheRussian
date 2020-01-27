from abc import abstractmethod

from dynamic_texture import DynamicTexture
from texture_asset import RenderOptions

class TileTexture(DynamicTexture):
    @abstractmethod
    def block_updated(self, world, at):
        pass

class SimpleTexture(TileTexture):
    def __init__(self, texture_asset):
        self.texture_asset = texture_asset

    def get_texture(self):
        return self.texture_asset

    def get_render_options(self):
        return RenderOptions((1, ))

    def block_updated(self, world, at):
        pass


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

        self.render_options = RenderOptions((1, ))

    def block_updated(self, world, at):
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

        if rotations == []:
            rotations = [1, 2, 4, 8]

        self.render_options = RenderOptions(tuple(rotations))

    def get_texture(self):
        return self.texture_asset

    def get_render_options(self):
        return self.render_options
