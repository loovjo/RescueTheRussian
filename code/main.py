import pygame
import world
import entity
import texture_asset
import time
import random

animation = texture_asset.WalkTexture(["humanRuRuFront.png", "humanRuRuFront1.png", "humanRuRuFront.png", "humanRuRuFront2.png"])

world = world.World()
human = entity.Human([0, 0], animation)
world.entities.append(human)

width, height = size = 1080, 800

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Rescue the russian")

acc = [0, 0]

last_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

    screen.fill((255, 255, 255))

    world.draw(screen)

    pygame.display.flip()

    dt = time.time() - last_time
    last_time = time.time()

    human.velocity[0] += acc[0] * dt * 50
    human.velocity[1] += acc[1] * dt * 50
    world.update(dt)
