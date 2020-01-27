from abc import ABC, abstractmethod

import texture_asset

class DynamicTexture(ABC):
    @abstractmethod
    def get_texture(self):
        pass

    @abstractmethod
    def get_render_options(self):
        pass

    def render(self, height):
        return self.get_texture().render(height, self.get_render_options())

