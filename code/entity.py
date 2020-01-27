import math
import dynamic_texture
import pygame

BOX_SIZE = 3

SLOW_DOWN = 10

DRAW_DEBUG_HITBOXES = False

BOUNCE_COEFFICIENT = 0.7

class Entity:
    def __init__(self, pos, texture):
        if not isinstance(texture, dynamic_texture.EntityTexture):
            raise TypeError("Texture must be an EntityTexture")

        self.pos = pos
        self.velocity = [0, 0]

        self.texture = texture

        self.width = 0.4
        self.height = 0.8

        self.mass = 1 # kg

    def update(self, world, dt):
        self.velocity[0] -= self.velocity[0] * dt * SLOW_DOWN
        self.velocity[1] -= self.velocity[1] * dt * SLOW_DOWN

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        self.texture.entity_moved(self.velocity)

        block_left, at = world.get_at((self.pos[0] - self.width / 2, self.pos[1]))
        if block_left.walk_on(self, world, at):
            self.pos[0] = math.ceil(self.pos[0] - self.width / 2) + self.width / 2
            self.velocity[0] *= -1

        block_up, at = world.get_at((self.pos[0], self.pos[1] - self.height / 2))
        if block_up.walk_on(self, world, at):
            self.pos[1] = math.ceil(self.pos[1] - self.height / 2) + self.height / 2
            self.velocity[1] *= -1

        block_right, at = world.get_at((self.pos[0] + self.width / 2, self.pos[1]))
        if block_right.walk_on(self, world, at):
            self.pos[0] = math.floor(self.pos[0] + self.width / 2) - self.width / 2
            self.velocity[0] *= -1

        block_down, at = world.get_at((self.pos[0], self.pos[1] + self.height / 2))
        if block_down.walk_on(self, world, at):
            self.pos[1] = math.floor(self.pos[1] + self.height / 2) - self.height / 2
            self.velocity[1] *= -1

        # Collide with other entities
        # TODO: Not very efficient to loop thrgouh all other entities, makes update O(n^2)
        # We could use some more efficient data structure for storing entities, with fast
        # queriyng for objects close to a point

        for other in world.entities:
            if other is self:
                continue

            if not self.collides_with(other):
                continue
            # Keep momentum: v1_1 * m1 + v2_1 * m2 = v1_2 * m1 + v2_2 * m2
            # Decrease energy: m1 * v1_1 ** 2 + m2 * v2_1 ** 2 = c * (m1 * v1_2 ** 2 + m2 * v2_2 ** 2)

            my_vel_after_x = BOUNCE_COEFFICIENT * other.mass * (other.velocity[0] - self.velocity[0]) + self.mass * self.velocity[0] + other.mass * other.velocity[0]
            my_vel_after_x /= self.mass + other.mass
            my_vel_after_y = BOUNCE_COEFFICIENT * other.mass * (other.velocity[1] - self.velocity[1]) + self.mass * self.velocity[1] + other.mass * other.velocity[1]
            my_vel_after_y /= self.mass + other.mass

            other_vel_after_x = BOUNCE_COEFFICIENT * self.mass * (self.velocity[0] - other.velocity[0]) + other.mass * other.velocity[0] + self.mass * self.velocity[0]
            other_vel_after_x /= self.mass + other.mass
            other_vel_after_y = BOUNCE_COEFFICIENT * self.mass * (self.velocity[1] - other.velocity[1]) + other.mass * other.velocity[1] + self.mass * self.velocity[1]
            other_vel_after_y /= self.mass + other.mass

            self.velocity = [my_vel_after_x, my_vel_after_y]
            other.velocity = [other_vel_after_x, other_vel_after_y]

            center_of_mass_x = (self.pos[0] * self.mass + other.pos[0] * other.mass) / (self.mass + other.mass)
            center_of_mass_y = (self.pos[1] * self.mass + other.pos[1] * other.mass) / (self.mass + other.mass)

            delta_position_x = self.pos[0] - center_of_mass_x
            delta_position_y = self.pos[1] - center_of_mass_y

            distance = (delta_position_x ** 2 + delta_position_y ** 2) ** 0.5
            delta_position_x /= distance
            delta_position_y /= distance

            my_delta_x = other.mass * delta_position_x / (self.mass + other.mass)
            my_delta_y = other.mass * delta_position_y / (self.mass + other.mass)

            other_delta_x = self.mass * delta_position_x / (self.mass + other.mass)
            other_delta_y = self.mass * delta_position_y / (self.mass + other.mass)

            # Binary search for distance for no collision
            max_colliding_distance = 0
            min_noncolliding_distance = 2 * (self.width + self.height + other.width + other.height)
            for i in range(20):
                distance_here = (max_colliding_distance + min_noncolliding_distance) / 2

                self.pos = [center_of_mass_x + my_delta_x * distance_here, center_of_mass_y + my_delta_y * distance_here]
                other.pos = [center_of_mass_x - other_delta_x * distance_here, center_of_mass_y - other_delta_y * distance_here]

                if self.collides_with(other):
                    max_colliding_distance = distance_here
                else:
                    min_noncolliding_distance = distance_here


    def collides_with(self, other):
        if other.pos[0] - other.width / 2 >= self.pos[0] + self.width / 2:
            # other left edge after our right edge
            return False

        if other.pos[0] + other.width / 2 <= self.pos[0] - self.width / 2:
            # other right edge before our left
            return False

        if other.pos[1] - other.height / 2 >= self.pos[1] + self.height / 2:
            # etc
            return False

        if other.pos[1] + other.height / 2 <= self.pos[1] - self.height / 2:
            # etc
            return False

        return True

    def draw(self, world, screen):
        top_left_corner = world.transform_position((self.pos[0] - 0.5, self.pos[1] - 0.5))
        bottom_right_corner = world.transform_position([self.pos[0] + 0.5, self.pos[1] + 0.5])

        height = int(bottom_right_corner[1] - top_left_corner[1])

        surf = self.texture.render(height)

        screen.blit(surf, top_left_corner)

        if DRAW_DEBUG_HITBOXES:
            texture_rect = pygame.Rect(
                *top_left_corner,
                bottom_right_corner[0] - top_left_corner[0],
                bottom_right_corner[1] - top_left_corner[1],
            )

            pygame.draw.rect(screen, (255, 0, 0), texture_rect, 1)

            coll_tlc = world.transform_position((self.pos[0] - self.width / 2, self.pos[1] - self.height / 2))
            coll_brc = world.transform_position((self.pos[0] + self.width / 2, self.pos[1] + self.height / 2))

            collision_rect = pygame.Rect(
                *coll_tlc,
                coll_brc[0] - coll_tlc[0],
                coll_brc[1] - coll_tlc[1],
            )

            pygame.draw.rect(screen, (0, 255, 0), collision_rect, 1)


class Human(Entity):
    pass

class Russian(Human):
    def __init__(self, pos, texture):
        super(Russian, self).__init__(pos, texture)

        self.mass = 50

class American(Human):
    def __init__(self, pos, texture):
        super(American, self).__init__(pos, texture)
        self.width = 0.6
        self.height = 0.8

        self.mass = 100


def make_player(pos):
    return Russian(pos, dynamic_texture.EntityTexture.load_walking_texture("RuRu"))

def make_american(pos):
    return American(pos, dynamic_texture.EntityTexture.load_walking_texture("AmAm"))
