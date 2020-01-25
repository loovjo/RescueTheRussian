from abc import ABC, abstractmethod

class TileTexture(ABC):
    @abstractmethod
    def get_texture_asset(self, world, at):
        pass

class SimpleTexture(TileTexture):
    def __init__(self, texture_asset):
        self.texture_asset = texture_asset

    def get_texture_asset(self, world, at):
        return self.texture_asset
