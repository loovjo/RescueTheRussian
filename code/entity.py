import math
import time
from typing import Any, Union

from entity_texture import EntityTexture
import texture_asset
import pygame
import random

from entity_texture import CrucibleTexture

BOX_SIZE = 3

SLOW_DOWN = 10

DRAW_DEBUG_HITBOXES = False

BOUNCE_COEFFICIENT = 0.7


class Entity:
    def __init__(self, pos, texture):
        if not isinstance(texture, EntityTexture):
            raise TypeError("Texture must be an EntityTexture")

        self.pos = pos
        self.velocity = [0, 0]

        self.texture = texture

        self.width = 0.4
        self.height = 0.8

        self.mass = 1  # kg

    def update(self, world, dt):
        self.update_texture(dt)
        self.update_posvel(dt)
        self.update_entity_collisions(world, dt)
        self.update_block_collisions(world, dt)

    def update_texture(self, dt):
        self.texture.entity_moved(self.velocity, dt)

    def update_posvel(self, dt):
        self.velocity[0] -= self.velocity[0] * dt * SLOW_DOWN
        self.velocity[1] -= self.velocity[1] * dt * SLOW_DOWN

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

    def update_block_collisions(self, world, dt):
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

    def update_entity_collisions(self, world, dt):
        # Collide with other entities
        # TODO: Not very efficient to loop thrgouh all other entities, makes update O(n^2)
        # We could use some more efficient data structure for storing entities, with fast
        # queriyng for objects close to a point

        for other in world.entities:
            if other is self:
                continue

            if not self.collides_with(other):
                continue

            self.on_collision(other, world)
            other.on_collision(self, world)

            # Keep momentum: v1_1 * m1 + v2_1 * m2 = v1_2 * m1 + v2_2 * m2
            # Decrease energy: m1 * v1_1 ** 2 + m2 * v2_1 ** 2 = c * (m1 * v1_2 ** 2 + m2 * v2_2 ** 2)

            my_vel_after_x = BOUNCE_COEFFICIENT * other.mass * (other.velocity[0] - self.velocity[0]) + self.mass * \
                             self.velocity[0] + other.mass * other.velocity[0]
            my_vel_after_x /= self.mass + other.mass
            my_vel_after_y = BOUNCE_COEFFICIENT * other.mass * (other.velocity[1] - self.velocity[1]) + self.mass * \
                             self.velocity[1] + other.mass * other.velocity[1]
            my_vel_after_y /= self.mass + other.mass

            other_vel_after_x = BOUNCE_COEFFICIENT * self.mass * (self.velocity[0] - other.velocity[0]) + other.mass * \
                                other.velocity[0] + self.mass * self.velocity[0]
            other_vel_after_x /= self.mass + other.mass
            other_vel_after_y = BOUNCE_COEFFICIENT * self.mass * (self.velocity[1] - other.velocity[1]) + other.mass * \
                                other.velocity[1] + self.mass * self.velocity[1]
            other_vel_after_y /= self.mass + other.mass

            self.velocity = [my_vel_after_x, my_vel_after_y]
            other.velocity = [other_vel_after_x, other_vel_after_y]

            center_of_mass_x = (self.pos[0] * self.mass + other.pos[0] * other.mass) / (self.mass + other.mass)
            center_of_mass_y = (self.pos[1] * self.mass + other.pos[1] * other.mass) / (self.mass + other.mass)

            delta_position_x = self.pos[0] - center_of_mass_x
            delta_position_y = self.pos[1] - center_of_mass_y

            distance: Union[float, Any] = (delta_position_x ** 2 + delta_position_y ** 2) ** 0.5
            try:
                delta_position_x /= distance
            except:
                delta_position_x = 1000
            try:
                delta_position_y /= distance
            except:
                delta_position_y = 1000

            my_delta_x = other.mass * delta_position_x / (self.mass + other.mass)
            my_delta_y = other.mass * delta_position_y / (self.mass + other.mass)

            other_delta_x = self.mass * delta_position_x / (self.mass + other.mass)
            other_delta_y = self.mass * delta_position_y / (self.mass + other.mass)

            # Binary search for distance for no collision
            max_colliding_distance = 0
            min_noncolliding_distance = 2 * (self.width + self.height + other.width + other.height)
            for i in range(20):
                distance_here = (max_colliding_distance + min_noncolliding_distance) / 2

                self.pos = [center_of_mass_x + my_delta_x * distance_here,
                            center_of_mass_y + my_delta_y * distance_here]
                other.pos = [center_of_mass_x - other_delta_x * distance_here,
                             center_of_mass_y - other_delta_y * distance_here]

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

    def on_collision(self, other, world):
        pass

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

class Tool(Entity):
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


class Swede(Human):
    def __init__(self, pos, texture):
        super(Swede, self).__init__(pos, texture)

        self.mass = 20
        self.height = 0.9

class Spoon(Tool):
    def __init__(self, pos, texture):
        super(Spoon, self).__init__(pos, texture)

        self.mass = 10

class Crucible(Entity):
    def __init__(self, pos, texture):
        super(Crucible, self).__init__(pos, texture)
        self.smelting = False
        self.width = 1
        self.height = 1

        self.mass = 500

    def smelt(self, rock):
        self.smelting = self.texture.crucible_next_texture()
        self.time_since_texture = time.time()

    def update(self, world, dt):
        self.update_texture(dt)
        self.update_posvel(dt)
        self.update_entity_collisions(world, dt)
        self.update_block_collisions(world, dt)
        if self.smelting and time.time() - self.time_since_texture > 2:
            self.smelting = self.texture.crucible_next_texture()
            self.time_since_texture = time.time()
            if not self.smelting:
                world.entities.append(make_spoon(self.pos))

class Flag(Entity):
    def update_texture(self, dt):
        self.texture.entity_moved([0, 4], dt)
        self.height = 0.5
        self.width = 1

        self.mass = 5

ROCK_SIZES = [0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1]
class Rock(Entity):
    def __init__(self, pos, texture):
        super(Rock, self).__init__(pos, texture)

        self.height = 0.4
        self.width = 0.4

        self.mass = 5

        self.size_frame = 0

    def on_collision(self, other, world):
        if isinstance(self, Rock) and isinstance(other, Rock) and self.mass == other.mass:
            world.remove_entity(other)
            self.mass += 5
            self.size_frame += 1

        if isinstance(self, Rock) and isinstance(other, Crucible) and not other.smelting:
            world.remove_entity(self)
            other.smelt(self)

    def update_texture(self, dt):
        self.texture.current_frame = self.size_frame
        self.height = self.width = ROCK_SIZES[self.size_frame]

def make_player(pos):
    return Russian(pos, EntityTexture.load_walking_texture("RuRu"))


def make_american(pos):
    return American(pos, EntityTexture.load_walking_texture("AmAm"))


def make_swede(pos):
    return Swede(pos, EntityTexture.load_walking_texture("SwSw", [0, 1, 0, 1]))

def make_spoon(pos):
    animation = [
        texture_asset.TextureAsset("spoon.png")
    ]
    entext = EntityTexture(*([animation] * 4))

    return Spoon(pos, entext)



def make_flag_am(pos):
    animation = [
        texture_asset.TextureAsset("US_Rendered/out{:04d}.png".format(i))
        for i in range(0, 50, 2)
    ]
    entext = EntityTexture(*([animation] * 4))

    return Flag(pos, entext)


def make_flag_sw(pos):
    animation = [
        texture_asset.TextureAsset("SW_Rendered/out{:04d}.png".format(i))
        for i in range(0, 50, 2)
    ]
    entext = EntityTexture(*([animation] * 4))

    return Flag(pos, entext)


def make_flag_ru(pos):
    animation = [
        texture_asset.TextureAsset("RU_Rendered/out{:04d}.png".format(i))
        for i in range(0, 50, 2)
    ]
    entext = EntityTexture(*([animation] * 4))

    return Flag(pos, entext)


def make_rock(pos, size=0):
    animation = [
        texture_asset.TextureAsset("rock{}.png".format(i))
        for i in range(10)
    ]

    entext = EntityTexture(*([animation] * 4))

    rock = Rock(pos, entext)
    rock.size_frame = size

    return rock

def make_crucible(pos):
    entext = CrucibleTexture()

    return Crucible(pos, entext)
