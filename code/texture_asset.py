import os
import pygame

TEXTURE_ASSETS_FOLDER = "assets/textures/"

class TextureAsset:
    def __init__(self, frame_names):
        self.frames = []

        for file_name in frame_names:
            path = os.path.join(TEXTURE_ASSETS_FOLDER, file_name)

            print("Loading texture", path)

            self.frames.append(pygame.image.load(path))

        self.current_frame = 0

        self.resize_cached = {} # {(height, frame): surface}

    def get_current_sized(self, height):
        self.current_frame %= len(self.frames)
        if (height, self.current_frame) in self.resize_cached:
            return self.resize_cached[(height, self.current_frame)]

        frame = self.frames[self.current_frame]

        scaled_width = height / frame.get_height() * frame.get_width()

        scaled = pygame.transform.scale(frame, (int(scaled_width), int(height)))

        self.resize_cached[(height, self.current_frame)] = scaled

        return scaled

WALK_TEXTURE_SPEED = 0.1

class WalkTexture(TextureAsset):
    def __init__(self, frame_names):
        super(WalkTexture, self).__init__(frame_names)

        self.frame_fpart = 0

    def walked(self, distance):
        self.frame_fpart += distance * WALK_TEXTURE_SPEED

        while self.frame_fpart > 1:
            self.current_frame += 1
            self.frame_fpart -= 1
