import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)

SPEED = 7
ACCELERATION = 1

game_run = False
rex_speed = 10
x_ground = 0

class Rex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rex_stop_images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex1.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex4.png').convert_alpha()
        ]
        self.rex_run_images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex2.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex3.png').convert_alpha()
        ]
        self.rex_down_images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex5.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/rex/rex6.png').convert_alpha()
        ]

        self.time = 0
        self.speed = SPEED
        self.rex_state = 'stop'

        self.current_image = 0
        self.image = self.rex_stop_images[0]

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH/2 - 300
        self.rect[1] = SCREEN_HEIGHT/2 - 16
    
    def update(self):
        if game_run:
            self.time += 1
            if self.rex_state == 'stop':
                self.image = self.rex_stop_images[0]
            else:
                if self.time % 3 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_run_images[self.current_image]
            
            if self.rect[1] >= SCREEN_HEIGHT/2 - 16:
                self.rex_state = 'running'
                self.speed = 0 
                if self.rect[3] < 40:
                    self.rex_state = 'shifting'
                    self.rect[1] = SCREEN_HEIGHT/2 - 16
                else:
                    self.rex_state = 'running'
            else:
                self.rex_state = 'bumping'
                self.speed += ACCELERATION

            self.rect[1] += self.speed 
        
    def bump(self):
        if self.rex_state != 'bumping' and self.rex_state != 'shifting':
            
            self.speed = -SPEED*2
            self.rect[1] += self.speed 

    def shift(self):
        if self.rex_state == 'running':
            self.time += 1
            if self.time % 3 == 0:
                self.current_image = (self.current_image + 1) % 2
                self.image = self.rex_down_images[self.current_image]
            


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

rex_group = pygame.sprite.Group()
rex = Rex()
rex_group.add(rex)



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
    clock.tick(30)
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_run = True
        rex.bump()
    elif keys[pygame.K_DOWN]:
        rex.shift()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    load_background(game_run)

    rex_group.update()

    rex_group.draw(screen)

    pygame.display.update()