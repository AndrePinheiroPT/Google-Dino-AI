import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)

class Rex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex2.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex3.png').convert_alpha()
        ]

        self.current_image = 0
        self.image = pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex1.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = SCREEN_HEIGHT/2 - 8
    
    def update(self):
        self.current_image = (self.current_image + 1) % 2
        self.image = self.images[self.current_image]


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

rex_group = pygame.sprite.Group()
rex = Rex()
rex_group.add(rex)

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
    clock.tick(10)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_run = True

    load_background(game_run)

    rex_group.update()

    rex_group.draw(screen)

    pygame.display.update()