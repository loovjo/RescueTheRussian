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

class TextureAsset:
    def __init__(self, frame_names):
        self.frames = []

        for file_name in frame_names:
            path = os.path.join(TEXTURE_ASSETS_FOLDER, file_name)

            print("Loading texture", path)

            self.frames.append(pygame.image.load(path))

        self.current_frame = 0

        self.resize_cached = {} # {(height, frame): surface}

    # Rotation masks is list of bitmassk rotations to be anded, where every result is ored
    def get_current_sized(self, height, rotation_masks=(1, )):
        height = int(height)
        self.current_frame %= len(self.frames)

        if (height, self.current_frame, rotation_masks) in self.resize_cached:
            return self.resize_cached[(height, self.current_frame, rotation_masks)]

        frame = None

        for rotation_mask in rotation_masks:
            here = None
            for i in range(4):
                if (rotation_mask >> i) & 1 == 1:
                    rotated = pygame.transform.rotate(self.frames[self.current_frame], i * 90)
                    if here == None:
                        here = rotated
                    else:
                        here = image_and(here, rotated)

            if here == None:
                here = self.frames[self.current_frame].copy()
                here.fill((0, 0, 0, 0))

            if frame == None:
                frame = here
            else:
                frame = image_or(frame, here)

        scaled_width = height / frame.get_height() * frame.get_width()
        scaled = pygame.transform.scale(frame, (int(scaled_width), int(height)))

        self.resize_cached[(height, self.current_frame, rotation_masks)] = scaled

        return scaled

WALK_TEXTURE_SPEED = 0.05

class WalkTexture(TextureAsset):
    def __init__(self, frame_names):
        super(WalkTexture, self).__init__(frame_names)

        self.frame_fpart = 0

    def walked(self, distance):
        self.frame_fpart += distance * WALK_TEXTURE_SPEED

        while self.frame_fpart > 1:
            self.current_frame += 1
            self.frame_fpart -= 1

