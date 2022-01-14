import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)

SPEED = 7
ACCELERATION = 1

GROUND_WIDTH = 2*SCREEN_WIDTH
GROUND_HEIGHT = 15

game_run = True
ground_speed = 10

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
            if self.rex_state == 'stop' or self.rex_state == 'bumping':
                self.image = self.rex_stop_images[0]
            elif self.rex_state == 'running': 
                if self.time % 3 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_run_images[self.current_image]
                    
            elif self.rex_state == 'shifting':
                if self.time % 3 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_down_images[self.current_image]

            self.rect[3] = self.image.get_rect()[3]

            if self.rect[1] >= SCREEN_HEIGHT/2 - 16 or self.rex_state == 'shifting':
                self.rex_state == 'running'
                self.rect[1] = SCREEN_HEIGHT/2 - 16
                self.speed = 0 
                if self.rect[3] < 40:
                    self.rex_state == 'shifting'
                    self.rect[1] = SCREEN_HEIGHT/2 + 3
            else:
                self.speed += ACCELERATION

            self.rect[1] += self.speed 
        
    def bump(self):
        if self.rex_state != 'bumping' and self.rex_state != 'shifting':
            self.rex_state = 'bumping'
            self.speed = -SPEED*2
            self.rect[1] += self.speed 
            
    def shift(self):
        if self.rex_state == 'running':
            self.rex_state = 'shifting'

class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/ground.png')
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = x

    def update(self):
        self.rect[0] -= ground_speed
        self.rect[1] = SCREEN_HEIGHT/2 + 20 

def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

rex_group = pygame.sprite.Group()
rex = Rex()
rex_group.add(rex)

ground_group = pygame.sprite.Group()
for i in range(0, 2):
    ground = Ground(GROUND_WIDTH*i)
    ground_group.add(ground)

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    if rex.rect[1] >= SCREEN_HEIGHT/2 - 16 and game_run:
        rex.rex_state = 'running'
    if keys[pygame.K_SPACE]:
        rex.bump()
    elif keys[pygame.K_DOWN]:
        rex.shift()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    rex_group.update()
    ground_group.update()

    rex_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()