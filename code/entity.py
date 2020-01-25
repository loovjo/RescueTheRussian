import math
import texture_asset

BOX_SIZE = 3

SLOW_DOWN = 10

MIN_VELOCITY = 0.2

class Entity:
    def __init__(self, pos, animation):
        self.pos = pos
        self.velocity = [0, 0]

        self.animation = animation

    def update(self, dt):
        self.velocity[0] -= self.velocity[0] * dt * SLOW_DOWN
        self.velocity[1] -= self.velocity[1] * dt * SLOW_DOWN

        if self.velocity[0]**2 + self.velocity[1]**2 < MIN_VELOCITY**2:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.animation = self.wa_front
            self.animation.current_frame = 0

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        total_velocity = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5

        self.animation.walked(total_velocity)

    def draw(self, world, screen):
        top_left_corner = world.transform_position((self.pos[0] - 0.5, self.pos[1] - 0.5))
        bottom_left_corner = world.transform_position([self.pos[0] - 0.5, self.pos[1] + 0.5])

        height = int(bottom_left_corner[1] - top_left_corner[1])

        surf = self.animation.get_current_sized(height)

        screen.blit(surf, top_left_corner)

class Human(Entity):
    def __init__(self, pos, wa_front, wa_left, wa_back, wa_right):
        super(Human, self).__init__(pos, wa_front)

        self.wa_front = wa_front
        self.wa_left = wa_left
        self.wa_back = wa_back
        self.wa_right = wa_right

    def update(self, dt):
        if abs(self.velocity[0]) > abs(self.velocity[1]):
            if self.velocity[0] > 0:
                self.animation = self.wa_right
            else:
                self.animation = self.wa_left
        else:
            if self.velocity[1] > 0:
                self.animation = self.wa_front
            else:
                self.animation = self.wa_back

        super().update(dt)

wa_front = texture_asset.WalkTexture(["humanRuRuFront0.png", "humanRuRuFront1.png", "humanRuRuFront0.png", "humanRuRuFront2.png"])
wa_left = texture_asset.WalkTexture(["humanRuRuLeft0.png", "humanRuRuLeft1.png", "humanRuRuLeft0.png", "humanRuRuLeft2.png"])
wa_back = texture_asset.WalkTexture(["humanRuRuBack0.png", "humanRuRuBack1.png", "humanRuRuBack0.png", "humanRuRuBack2.png"])
wa_right = texture_asset.WalkTexture(["humanRuRuRight0.png", "humanRuRuRight1.png", "humanRuRuRight0.png", "humanRuRuRight2.png"])

PLAYER = Human([1, 1], wa_front, wa_left, wa_back, wa_right)
