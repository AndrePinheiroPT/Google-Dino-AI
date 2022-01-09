import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

game_run = False
rex_speed = 5
x_ground = 0

def load_background(running = False):
    global rex_speed, x_ground
    img_ground = pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/ground.png')
    if running:
        x_ground -= rex_speed
    if abs(x_ground) > img_ground.get_width():
        x_ground = 0
    screen.blit(img_ground, (x_ground, 270))
    screen.blit(img_ground, (img_ground.get_width() + x_ground, 270))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_run = True

    load_background(game_run)
    print(game_run)

    pygame.display.update()