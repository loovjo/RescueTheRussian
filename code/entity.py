BOX_SIZE = 5

class Entity:
    def __init__(self, pos, animation):
        self.pos = pos
        self.velocity = [0, 0]

        self.animation = animation

    def update(self, dt):
        self.velocity[0] *= 0.1 ** dt
        self.velocity[1] *= 0.1 ** dt

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        total_velocity = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5

        self.animation.walked(total_velocity)

        if self.pos[0] > BOX_SIZE:
            self.velocity[0] *= -1
            self.pos[0] = BOX_SIZE

        if self.pos[0] < -BOX_SIZE:
            self.velocity[0] *= -1
            self.pos[0] = -BOX_SIZE

        if self.pos[1] > BOX_SIZE:
            self.velocity[1] *= -1
            self.pos[1] = BOX_SIZE

        if self.pos[1] < -BOX_SIZE:
            self.velocity[1] *= -1
            self.pos[1] = -BOX_SIZE

    def draw(self, world, screen):
        top_left_corner = world.transform_position((self.pos[0] - 0.5, self.pos[1] - 0.5))
        bottom_left_corner = world.transform_position([self.pos[0] - 0.5, self.pos[1] + 0.5])

        height = int(bottom_left_corner[1] - top_left_corner[1])

        surf = self.animation.get_current_sized(height)

        screen.blit(surf, top_left_corner)

class Human(Entity):
    def __init__(self, pos, walking_animation):
        super(Human, self).__init__(pos, walking_animation)
