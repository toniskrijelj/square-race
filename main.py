import pygame
import car
import map

pygame.init()
screen = pygame.display.set_mode([1000, 800])

FPS = 60

clock = pygame.time.Clock()

car.generate_cars()

refresh = True
running = True
FPS_lock = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                car.new_generation()
            if event.key == pygame.K_o:
                map.change_map()
                car.refresh()
            if event.key == pygame.K_r:
                car.generate_cars()
            if event.key == pygame.K_q:
                refresh = not refresh
            if event.key == pygame.K_l:
                FPS_lock = not FPS_lock

        if event.type == pygame.MOUSEBUTTONDOWN:
            map.set_spawn_point(pygame.mouse.get_pos())
            car.refresh()

    car.update()

    if refresh:
        screen.fill((255, 255, 255))
        map.draw(screen)
        car.draw(screen)
        pygame.display.flip()

    if FPS_lock:
        clock.tick(FPS)

pygame.quit()
