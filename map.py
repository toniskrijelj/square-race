import pygame

spawn_x = 100
spawn_y = 450

background_imgs = [
    pygame.image.load('Images/Sprites/background.png'),
    pygame.image.load('Images/Sprites/background2.png'),
    pygame.image.load('Images/Sprites/background3.png'),
    pygame.image.load('Images/Sprites/background4.png'),
    pygame.image.load('Images/Sprites/background5.png'),
    pygame.image.load('Images/Sprites/background6.png'),
    pygame.image.load('Images/Sprites/background7.png'),
    pygame.image.load('Images/Sprites/background8.png'),
    pygame.image.load('Images/Sprites/background9.png')]

background_num = 0
background_img = background_imgs[0]
background_rect = background_img.get_rect()
background_arr = pygame.surfarray.array2d(background_img)


def outside(pos):
    return background_arr[int(pos[0])][int(pos[1])] == background_arr[0][0]


def draw(screen):
    screen.blit(background_img, background_rect)


def change_map():
    global background_num, background_img, background_rect, background_arr
    background_num = (background_num + 1) % len(background_imgs)
    background_img = background_imgs[background_num]
    background_rect = background_img.get_rect()
    background_arr = pygame.surfarray.array2d(background_img)


def set_spawn_point(pos):
    global spawn_x
    global spawn_y
    spawn_x, spawn_y = pos
