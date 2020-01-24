import pygame
import World
import entity
import texture_asset
import time
import random

animation = texture_asset.WalkTexture(["humanAmAmFront0.png", "humanAmAmFront1.png", "humanAmAmFront0.png", "humanAmAmFront2.png"])

world = World.World()
human = entity.Human([0, 0], animation)
world.entities.append(human)

width, height = size = 1080, 800

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Rescue the russian")

acc = [0, 0]

last_time = time.time()

black = pygame.Surface((screen.get_width(), screen.get_height()))
black.set_alpha(30)
black.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                acc[0] -= 1
            if event.key == pygame.K_RIGHT:
                acc[0] += 1
            if event.key == pygame.K_UP:
                acc[1] -= 1
            if event.key == pygame.K_DOWN:
                acc[1] += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                acc[0] += 1
            if event.key == pygame.K_RIGHT:
                acc[0] -= 1
            if event.key == pygame.K_UP:
                acc[1] += 1
            if event.key == pygame.K_DOWN:
                acc[1] -= 1

    if random.random() < 0.4:
        screen.blit(black, (0, 0))

    world.draw(screen)

    pygame.display.flip()

    dt = time.time() - last_time
    last_time = time.time()

    human.velocity[0] += acc[0] * dt * 20
    human.velocity[1] += acc[1] * dt * 20
    world.update(dt)
