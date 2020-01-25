import math
import texture_asset

BOX_SIZE = 3

SLOW_DOWN = 10

class Entity:
    def __init__(self, pos, animation):
        self.pos = pos
        self.velocity = [0, 0]

        self.animation = animation

        self.width = 0.4
        self.height = 0.8

    def update(self, world, dt):
        self.velocity[0] -= self.velocity[0] * dt * SLOW_DOWN
        self.velocity[1] -= self.velocity[1] * dt * SLOW_DOWN

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        total_velocity = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5

        self.animation.walked(total_velocity)

        block_left = world.get_at((self.pos[0] - self.width / 2, self.pos[1]))
        if block_left.walk_on(self):
            self.pos[0] = math.ceil(self.pos[0] - self.width / 2) + self.width / 2
            self.velocity[0] *= -1

        block_up = world.get_at((self.pos[0], self.pos[1] - self.height / 2))
        if block_up.walk_on(self):
            self.pos[1] = math.ceil(self.pos[1] - self.height / 2) + self.height / 2
            self.velocity[1] *= -1

        block_right = world.get_at((self.pos[0] + self.width / 2, self.pos[1]))
        if block_right.walk_on(self):
            self.pos[0] = math.floor(self.pos[0] + self.width / 2) - self.width / 2
            self.velocity[0] *= -1

        block_down = world.get_at((self.pos[0], self.pos[1] + self.height / 2))
        if block_down.walk_on(self):
            self.pos[1] = math.floor(self.pos[1] + self.height / 2) - self.height / 2
            self.velocity[1] *= -1

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

    def update(self, world, dt):
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

        super().update(world, dt)

wa_front = texture_asset.WalkTexture(["humanRuRuFront0.png", "humanRuRuFront1.png", "humanRuRuFront0.png", "humanRuRuFront2.png"])
wa_left = texture_asset.WalkTexture(["humanRuRuLeft0.png", "humanRuRuLeft1.png", "humanRuRuLeft0.png", "humanRuRuLeft2.png"])
wa_back = texture_asset.WalkTexture(["humanRuRuBack0.png", "humanRuRuBack1.png", "humanRuRuBack0.png", "humanRuRuBack2.png"])
wa_right = texture_asset.WalkTexture(["humanRuRuRight0.png", "humanRuRuRight1.png", "humanRuRuRight0.png", "humanRuRuRight2.png"])

PLAYER = Human([2, 2], wa_front, wa_left, wa_back, wa_right)
