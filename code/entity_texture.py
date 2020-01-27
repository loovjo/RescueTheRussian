from dynamic_texture import DynamicTexture
import texture_asset

MIN_VELOCITY = 0.04
WALK_CHANGE_SPEED = 10

class EntityTexture(DynamicTexture):
    def __init__(self, f_frames, l_frames, d_frames, r_frames, wa_speed=0.05):
        self.frames = [f_frames, l_frames, d_frames, r_frames]

        self.current_direction = 0
        self.current_frame = 0.0
        self.wa_speed = wa_speed

        self.average_velocity = [0, 0]

    def get_texture_asset(self):
        return self.frames[self.current_direction][int(self.current_frame)]

    def entity_moved(self, velocity, dt):
        self.average_velocity = [
            self.average_velocity[0] * (1 - WALK_CHANGE_SPEED * dt) + velocity[0] * WALK_CHANGE_SPEED * dt,
            self.average_velocity[1] * (1 - WALK_CHANGE_SPEED * dt) + velocity[1] * WALK_CHANGE_SPEED * dt,
        ]

        if abs(self.average_velocity[0]) > abs(self.average_velocity[1]): # Moves in x
            self.current_direction = 3 if self.average_velocity[0] > 0 else 1
        else: # Moves in y
            self.current_direction = 0 if self.average_velocity[1] > 0 else 2

        speed = (self.average_velocity[0] ** 2 + self.average_velocity[1] ** 2) ** 0.5
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
