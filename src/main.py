from curses import KEY_DOWN
from pickle import POP
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

        self.dist = 0
        self.fitness = 0

        self.inputs = None
        
        self.w1 = np.random.randint(-1000, 1001, size=(5, 5))
        self.b1 = np.random.randint(-1000, 1001, size=(5, 1))

        self.w2 = np.random.randint(-1000, 1001, size=(2, 5))
        self.b2 = np.random.randint(-1000, 1001, size=(2, 1))

        self.hidden = np.zeros(5)

        self.time = 0
        self.speed = SPEED
        self.state = 'bumping'

        self.current_image = 0
        self.image = self.rex_stop_images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH/2 - 300 + random.randint(-25, 25)
        self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])

    def feed_forward(self):
        self.hidden = relu(self.w1.dot(self.inputs)[np.newaxis].transpose() + self.b1)
        output = relu(self.w2.dot(self.hidden) + self.b2)
        return output

    def update(self):
        if self.state != 'dead':
            self.time += 1
            if self.state == 'bumping':
                self.image = self.rex_stop_images[0]
            elif self.state == 'running': 
                if self.time % 5 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_run_images[self.current_image]
                    
            elif self.state == 'shifting':
                if self.time % 5 == 0:
                    self.current_image = (self.current_image + 1) % 2
                    self.image = self.rex_down_images[self.current_image]

            self.rect[3] = self.image.get_rect()[3]
            self.mask = pygame.mask.from_surface(self.image)

            if self.rect[1] >= SCREEN_HEIGHT/2 + (35 - self.rect[3]) or self.state == 'shifting':
                self.state == 'running'
                self.rect[1] = SCREEN_HEIGHT/2 + (35 - self.rect[3])
                self.speed = 0 
                if self.rect[3] < 40:
                    self.state == 'shifting'
            else:
                self.speed += ACCELERATION

            self.rect[1] += self.speed
        else: 
            self.rect[0] -= ground_speed
    
    def set_inputs(self, inputs):
        self.inputs = np.array(inputs)

    def bump(self):
        if self.state != 'bumping' and self.state != 'shifting' and self.state != 'dead':
            self.state = 'bumping'
            self.speed = -SPEED*2
            self.rect[1] += self.speed 
            
    def shift(self):
        if self.state == 'running' and self.state != 'dead':
            self.state = 'shifting'

    def dead(self):
        self.state = 'dead'
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
distance = 1
def reset_game(randomic=False):
    global rex_group, ground_group, obstacle_group, distance
    
    rex_group = start_population(Rex) if randomic else new_generation(rex_group, distance, Rex)
    distance = 1

    ground_group = pygame.sprite.Group()
    for i in range(0, 2):
        ground = Ground(GROUND_WIDTH*i)
        ground_group.add(ground)

    obstacle_group = pygame.sprite.Group()
    for i in range(0, 2):
        cactus = Cactus(SCREEN_WIDTH + i*OBSTACLE_GAP, random.randint(0, 1))
        obstacle_group.add(cactus)


reset_game(True) 

clock = pygame.time.Clock()
while True:
    clock.tick(50)
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(obstacle_group.sprites()[0]):
        obstacle_group.remove(obstacle_group.sprites()[0])
        if random.randint(0, 1) and distance > 500:
            new_obstacle = Bird(OBSTACLE_GAP*2 + random.randint(-70, 70), random.randint(0, 2)*40) 
        else:
            new_obstacle = Cactus(OBSTACLE_GAP*2 + random.randint(-70, 70), random.randint(0, 1)) 
        obstacle_group.add(new_obstacle)

    get_senses(rex_group, obstacle_group, [ground_speed])
    population_dead = 0
    for rex in rex_group.sprites():
        outputs = rex.feed_forward()

        if rex.rect[1] >= SCREEN_HEIGHT/2 - 15 and rex.state != 'dead':
            rex.state = 'running'
        if outputs[0] > 0:
            rex.bump()
        elif outputs[1] > 0:
            rex.shift() 

        if pygame.sprite.spritecollideany(rex, obstacle_group, pygame.sprite.collide_mask):
            rex.dead()

        if rex.state == 'dead':
            population_dead += 1
            if is_off_screen(rex):
                rex.rect[0] = SCREEN_WIDTH
                rex.rect[1] = SCREEN_HEIGHT
        else:
            rex.dist = distance
            
    if population_dead == POPULATION_LENGTH:
        reset_game()

    rex_group.update()
    ground_group.update()
    obstacle_group.update()

    rex_group.draw(screen)
    ground_group.draw(screen)
    obstacle_group.draw(screen)
    
    distance += ground_speed
    pygame.display.update()