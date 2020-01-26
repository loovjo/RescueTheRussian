import math
import texture_asset
import pygame

BOX_SIZE = 3

SLOW_DOWN = 10

MIN_VELOCITY = 0.04

DRAW_DEBUG_HITBOXES = False

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

        if self.velocity[0]**2 + self.velocity[1]**2 < MIN_VELOCITY:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.animation = self.wa_front
            self.animation.current_frame = 0

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        total_velocity = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5

        self.animation.walked(total_velocity)

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

    def draw(self, world, screen):
        top_left_corner = world.transform_position((self.pos[0] - 0.5, self.pos[1] - 0.5))
        bottom_right_corner = world.transform_position([self.pos[0] + 0.5, self.pos[1] + 0.5])

        height = int(bottom_right_corner[1] - top_left_corner[1])

        surf = self.animation.get_current_sized(height)

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

class Russian(Human):
    pass

class American(Human):
    def __init__(self, pos, wa_front, wa_left, wa_back, wa_right):
        super(American, self).__init__(pos, wa_front, wa_left, wa_back, wa_right)
        self.width = 0.6
        self.height = 0.8

wa_ru_front = texture_asset.WalkTexture(["humanRuRuFront0.png", "humanRuRuFront1.png", "humanRuRuFront0.png", "humanRuRuFront2.png"])
wa_ru_left = texture_asset.WalkTexture(["humanRuRuLeft0.png", "humanRuRuLeft1.png", "humanRuRuLeft0.png", "humanRuRuLeft2.png"])
wa_ru_back = texture_asset.WalkTexture(["humanRuRuBack0.png", "humanRuRuBack1.png", "humanRuRuBack0.png", "humanRuRuBack2.png"])
wa_ru_right = texture_asset.WalkTexture(["humanRuRuRight0.png", "humanRuRuRight1.png", "humanRuRuRight0.png", "humanRuRuRight2.png"])

def make_player(pos):
    return Russian(pos, wa_ru_front, wa_ru_left, wa_ru_back, wa_ru_right)

wa_am_front = texture_asset.WalkTexture(["humanAmAmFront0.png", "humanAmAmFront1.png", "humanAmAmFront0.png", "humanAmAmFront2.png"])
wa_am_left = texture_asset.WalkTexture(["humanAmAmLeft0.png", "humanAmAmLeft1.png", "humanAmAmLeft0.png", "humanAmAmLeft2.png"])
wa_am_back = texture_asset.WalkTexture(["humanAmAmBack0.png", "humanAmAmBack1.png", "humanAmAmBack0.png", "humanAmAmBack2.png"])
wa_am_right = texture_asset.WalkTexture(["humanAmAmRight0.png", "humanAmAmRight1.png", "humanAmAmRight0.png", "humanAmAmRight2.png"])

def make_american(pos):
    return American(pos, wa_am_front, wa_am_left, wa_am_back, wa_am_right)
