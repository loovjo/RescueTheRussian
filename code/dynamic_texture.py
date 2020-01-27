from abc import ABC, abstractmethod

import texture_asset

class DynamicTexture(ABC):
    @abstractmethod
    def get_texture_asset(self):
        pass

    @abstractmethod
    def get_render_options(self):
        pass

    def render(self, height):
        return self.get_texture_asset().render(height, self.get_render_options())

