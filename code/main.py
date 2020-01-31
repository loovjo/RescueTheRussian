import pygame
import world
import entity
import texture_asset
import time
import random

world = world.World()
#world.entities.append(entity.make_player([2, 2]))

width, height = size = 800, 600

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Rescue the russian")

acc = [0, 0]

last_time = time.time()
last_dts = []

time_since_debug_print = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                acc[0] -= 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                acc[0] += 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                acc[1] -= 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                acc[1] += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                acc[0] += 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                acc[0] -= 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                acc[1] += 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                acc[1] -= 1

    dt = time.time() - last_time
    last_time = time.time()
    if dt < 1 / 60:
        time.sleep(1 / 60 - dt)
        dt = 1 / 60


    human = world.entities[world.get_player_idx()]
    human.velocity[0] += acc[0] * dt * 50
    human.velocity[1] += acc[1] * dt * 50

    udt = dt
    while udt > 1 / 60:
        world.update(1 / 60)
        udt -= 1 / 60
    world.update(udt)

    screen.fill((0, 0, 0))

    world.draw(screen)

    pygame.display.flip()

    last_dts.append(dt)

    if time.time() - time_since_debug_print > 1:
        time_since_debug_print = time.time()
        average_dt = sum(last_dts) / len(last_dts)
        last_dts = []
        print("FPS: {:.4}".format(1 / average_dt))

