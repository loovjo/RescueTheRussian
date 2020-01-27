import os
import pygame

TEXTURE_ASSETS_FOLDER = "assets/textures/"

def get_factor(color):
    avg_color = (color.r + color.g + color.b) / 3
    std_sqr = (color.r - avg_color) ** 2 + (color.g - avg_color) ** 2 + (color.b - avg_color) ** 2

    return 1 / (std_sqr + 0.0001)

def image_and(surface_1, surface_2):
    result = surface_1.copy()
    for y in range(surface_1.get_height()):
        for x in range(surface_1.get_width()):
            color_1 = surface_1.get_at((x, y))
            color_2 = surface_2.get_at((x, y))

            total_a = color_1.a + color_2.a
            if total_a == 0:
                continue

            factor_1 = get_factor(color_1)
            factor_2 = get_factor(color_2)

            total_factor = factor_1 + factor_2

            res_a = color_1.a * color_2.a / 256
            res_r = (color_1.r * factor_1 + color_2.r * factor_2) / total_factor
            res_g = (color_1.g * factor_1 + color_2.g * factor_2) / total_factor
            res_b = (color_1.b * factor_1 + color_2.b * factor_2) / total_factor

            res_col = pygame.Color(int(res_r), int(res_g), int(res_b), int(res_a))
            result.set_at((x, y), res_col)

    return result

def image_or(surface_1, surface_2):
    result = surface_1.copy()
    for y in range(surface_1.get_height()):
        for x in range(surface_1.get_width()):
            color_1 = surface_1.get_at((x, y))
            color_2 = surface_2.get_at((x, y))

            total_a = color_1.a + color_2.a
            if total_a == 0:
                continue

            factor_1 = color_1.a
            factor_2 = color_2.a

            total_factor = factor_1 + factor_2

            res_a = 255 - (255 - color_1.a) * (255 - color_2.a) / 256
            res_r = (color_1.r * factor_1 + color_2.r * factor_2) / total_factor
            res_g = (color_1.g * factor_1 + color_2.g * factor_2) / total_factor
            res_b = (color_1.b * factor_1 + color_2.b * factor_2) / total_factor

            res_col = pygame.Color(int(res_r), int(res_g), int(res_b), int(res_a))
            result.set_at((x, y), res_col)

    return result

class RenderOptions:
    def __init__(self, rotation_masks):
        self.rotation_masks = rotation_masks

    def __hash__(self):
        return hash(self.rotation_masks)

RENDERED_CACHE = {} # {(name, height, hash(renderopts)): pygame surface}

class TextureAsset:
    def __init__(self, frame_name):
        print("Loading", frame_name)
        path = os.path.join(TEXTURE_ASSETS_FOLDER, frame_name)
        self.original_surface = pygame.image.load(path)

        self.name = frame_name

    # Rotation masks is list of bitmassk rotations to be anded, where every result is ored
    def render(self, height, render_options):
        height = int(height)

        if (self.name, height, hash(render_options)) in RENDERED_CACHE:
            return RENDERED_CACHE[(self.name, height, hash(render_options))]

        rendered = None

        for rotation_mask in render_options.rotation_masks:
            here = None
            for i in range(4):
                if (rotation_mask >> i) & 1 == 1:
                    rotated = pygame.transform.rotate(self.original_surface, i * 90)
                    if here == None:
                        here = rotated
                    else:
                        here = image_and(here, rotated)

            if here == None:
                here = self.original_surface.copy()
                here.fill((0, 0, 0, 0))

            if rendered == None:
                rendered = here
            else:
                rendered = image_or(rendered, here)

        if rendered == None:
            rendered = self.original_surface.copy()
            # Should we do anything here?
            rendered.fill((0, 0, 0, 0))

        scaled_width = height / rendered.get_height() * rendered.get_width()
        scaled = pygame.transform.scale(rendered, (int(scaled_width), int(height)))

        RENDERED_CACHE[(self.name, height, hash(render_options))] = scaled

        return scaled

