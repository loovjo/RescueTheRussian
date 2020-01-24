import pygame

width, height = size = 1080, 800

pygame.init()

screen = pygame.display.set_mode(size)
screen.fill((255,0,0))

pygame.display.set_caption("Rescue the russian")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.flip()
