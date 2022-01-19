from curses import KEY_DOWN
from tkinter import HIDDEN
import pygame, random
from pygame.locals import *
import numpy as np
from neural_network import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)

SPEED = 7
ACCELERATION = 1

GROUND_WIDTH = 2*SCREEN_WIDTH
GROUND_HEIGHT = 15

OBSTACLE_GAP = SCREEN_WIDTH*0.75

game_run = True
ground_speed = 8

class Rex(pygame.sprite.Sprite):
    def __init__(self, id):
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

        self.id = id
        self.inputs = None
        self.weights_layer1 = np.random.rand(5, 5)
        self.bias_layer1 = np.random.rand(5, 1)

        self.weights_layer2 = np.random.rand(2, 5)
        self.bias_layer2 = np.random.rand(2, 1)

        self.hidden = np.zeros(5)

        self.time = 0
        self.speed = SPEED
        self.rex_state = 'bumping'

        self.current_image = 0
        self.image = self.rex_stop_images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH/2 - 300 + random.randint(-25, 25)
        self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])

    def feed_forward(self):
        self.hidden = relu(self.weights_layer1.dot(self.inputs)[np.newaxis].transpose() + self.bias_layer1)
        output = relu(self.weights_layer2.dot(self.hidden) + self.bias_layer2)
        return output

    def update(self):
        if self.rex_state != 'dead':
            self.time += 1
            if self.rex_state == 'bumping':
                self.image = self.rex_stop_images[0]
            elif self.rex_state == 'running': 
                if self.time % 5 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_run_images[self.current_image]
                    
            elif self.rex_state == 'shifting':
                if self.time % 5 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_down_images[self.current_image]

            self.rect[3] = self.image.get_rect()[3]
            self.mask = pygame.mask.from_surface(self.image)

            if self.rect[1] >= SCREEN_HEIGHT/2 + (35 - self.rect[3]) or self.rex_state == 'shifting':
                self.rex_state == 'running'
                self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])
                self.speed = 0 
                if self.rect[3] < 40:
                    self.rex_state == 'shifting'
            else:
                self.speed += ACCELERATION

            self.rect[1] += self.speed 
    
    def set_inputs(self, inputs):
        self.inputs = np.array(inputs)

    def bump(self):
        if self.rex_state != 'bumping' and self.rex_state != 'shifting':
            self.rex_state = 'bumping'
            self.speed = -SPEED*2
            self.rect[1] += self.speed 
            
    def shift(self):
        if self.rex_state == 'running':
            self.rex_state = 'shifting'

    def dead(self):
        self.rex_state == 'dead'
        self.image = self.rex_stop_images[1]
        self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])

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

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x, is_big):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/big-cactus-1.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/big-cactus-2.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/big-cactus-3.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/little-cactus-1.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/little-cactus-2.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/cactus/little-cactus-3.png').convert_alpha(),
        ]

        self.image = self.images[random.randint(0, 2) if is_big else random.randint(3, 5)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])
        self.h = self.rect[1]
    
    def update(self):
        self.rect[0] -= ground_speed

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, h):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/bird/bird1.png').convert_alpha(),
            pygame.image.load(r'/home/pi/Documents/GitProjects/T-Rex/assets/bird/bird2.png').convert_alpha()
        ]

        self.time = 0
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3]) - h
        self.h = h
    
    def update(self):
        if self.time % 3 == 0:
            self.current_image = (self.current_image + 1) % 2
            self.image = self.images[self.current_image]
        self.time += 1
        self.rect[0] -= ground_speed
        

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]

rex_group = ground_group = obstacle_group = None
distance = 0
def reset_game():
    global rex_group, ground_group, obstacle_group, distance
    distance = 0
    rex_group = start_population(Rex)

    ground_group = pygame.sprite.Group()
    for i in range(0, 2):
        ground = Ground(GROUND_WIDTH*i)
        ground_group.add(ground)

    obstacle_group = pygame.sprite.Group()
    for i in range(0, 2):
        cactus = Cactus(SCREEN_WIDTH + i*OBSTACLE_GAP, random.randint(0, 1))
        obstacle_group.add(cactus)


reset_game() 
       
clock = pygame.time.Clock()
while True:
    clock.tick(50)
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE and not game_run:
                game_run = True
                reset_game()

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(obstacle_group.sprites()[0]):
        obstacle_group.remove(obstacle_group.sprites()[0])
        if random.randint(0, 1) and distance > 500:
            new_obstacle = Bird(OBSTACLE_GAP*2 + random.randint(-70, 70), random.randint(0, 2)*32) 
        else:
            new_obstacle = Cactus(OBSTACLE_GAP*2 + random.randint(-70, 70), random.randint(0, 1)) 
        obstacle_group.add(new_obstacle)

    if game_run:
        rex_group.update()
        ground_group.update()
        obstacle_group.update()

    rex_group.draw(screen)
    ground_group.draw(screen)
    obstacle_group.draw(screen)

    get_senses(rex_group, obstacle_group, [ground_speed])
    for rex in rex_group.sprites():
        outputs = rex.feed_forward()

        if rex.rect[1] >= SCREEN_HEIGHT/2 - 15:
            rex.rex_state = 'running'
        if outputs[0] > 0:
            rex.bump()
        elif outputs[1] > 0:
            rex.shift() 

        if pygame.sprite.spritecollideany(rex, obstacle_group, pygame.sprite.collide_mask):
            rex.dead()
    
    distance += ground_speed
    pygame.display.update()