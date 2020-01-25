import math

import pygame
import texture_asset

class Tile:
    def __init__(self, texture):
        self.texture = texture

    def draw(self, screen, world, at):
        top_left_corner = world.transform_position((at[0] - 0.5, at[1] - 0.5))
        bottom_right_corner = world.transform_position((at[0] + 0.5, at[1] + 0.5))

        rect = pygame.Rect(
            *top_left_corner,
            bottom_right_corner[0] - top_left_corner[0],
            bottom_right_corner[1] - top_left_corner[1],
        )

        if not rect.colliderect(screen.get_rect()):
            return

        height = math.ceil(bottom_right_corner[1] - top_left_corner[1])

        surf = self.texture.get_current_sized(height)

        screen.blit(surf, top_left_corner)

GROUND = Tile(texture_asset.TextureAsset(["floorWood.png"]))
