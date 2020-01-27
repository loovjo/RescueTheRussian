from dynamic_texture import DynamicTexture
import texture_asset

MIN_VELOCITY = 0.04

class EntityTexture(DynamicTexture):
    def __init__(self, f_frames, l_frames, d_frames, r_frames, wa_speed=0.05):
        self.frames = [f_frames, l_frames, d_frames, r_frames]

        self.current_direction = 0
        self.current_frame = 0.0
        self.wa_speed = wa_speed

    def get_texture(self):
        return self.frames[self.current_direction][int(self.current_frame)]

    def entity_moved(self, velocity):
        speed = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        if speed > 0.5:
            if abs(velocity[0]) > abs(velocity[1]): # Moves in x
                self.current_direction = 3 if velocity[0] > 0 else 1
            else: # Moves in y
                self.current_direction = 0 if velocity[1] > 0 else 2
        if speed < MIN_VELOCITY:
            self.current_direction = 0
            self.current_frame = 0

        self.current_frame = (self.current_frame + speed * self.wa_speed) % len(self.frames[self.current_direction])

    def load_walking_texture(entity_name):
        direction_animations = [
            [
                texture_asset.TextureAsset("human{}{}{}.png".format(entity_name, direction, i))
                for i in [0, 1, 0, 2]
            ]
            for direction in ["Front", "Left", "Back", "Right"]
        ]
        return EntityTexture(*direction_animations)

    def get_render_options(self):
        return texture_asset.RenderOptions((1, ))
