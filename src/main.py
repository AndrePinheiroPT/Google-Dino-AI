from pygame.locals import *
from draw import *
from neural_network import *
import pygame, random
import numpy as np
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)

SPEED = 7
ACCELERATION = 1

GROUND_WIDTH = 2*SCREEN_WIDTH
GROUND_HEIGHT = 15
GROUND_Y = round(7*SCREEN_HEIGHT/8)

OBSTACLE_GAP = SCREEN_WIDTH*0.80
PRINT_LIMIT = 100

NEURON_GAP_X = 100
NEURON_GAP_Y = 10
NEURON_RADIUS = 20

ground_speed = 8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('T-Rex')
pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

current_path = os.path.dirname(__file__)
rex_path = os.path.join(os.path.join(current_path, 'assets'), 'rex')
bird_path = os.path.join(os.path.join(current_path, 'assets'), 'bird')
cactus_path = os.path.join(os.path.join(current_path, 'assets'), 'cactus')

gap_neuron_text = 0
generation = 0
avarage_fitness = 0
rex_group = ground_group = obstacle_group = generation_group = None
highest_distance = 0
distance = 1

class Rex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rex_stop_images = [
            pygame.image.load(os.path.join(rex_path, 'rex1.png')).convert_alpha(),
            pygame.image.load(os.path.join(rex_path, 'rex4.png')).convert_alpha()
        ]
        self.rex_run_images = [
            pygame.image.load(os.path.join(rex_path, 'rex2.png')).convert_alpha(),
            pygame.image.load(os.path.join(rex_path, 'rex3.png')).convert_alpha()
        ]
        self.rex_down_images = [
            pygame.image.load(os.path.join(rex_path, 'rex5.png')).convert_alpha(),
            pygame.image.load(os.path.join(rex_path, 'rex6.png')).convert_alpha()
        ]

        self.fitness = 0
        self.inputs = self.ref_inputs = None
        
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
        self.rect[0] = SCREEN_WIDTH/2 - 300 + random.randint(-30, 30)
        self.rect[1] = GROUND_Y - self.rect[3] 

    def feed_forward(self):
        self.hidden = relu(self.w1.dot(self.inputs)[np.newaxis].transpose() + self.b1)
        output = relu(self.w2.dot(self.hidden) + self.b2)
        return output

    def update(self):
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
        if self.rect[1] >= GROUND_Y - self.rect[3]  or self.state == 'shifting':
            self.state = 'running'
            self.rect[1] = GROUND_Y - self.rect[3]
            self.speed = 0 
            if self.rect[3] < 40:
                self.state = 'shifting'
        else:
            self.speed += ACCELERATION

        self.rect[1] += self.speed
    
    def set_inputs(self, inputs, ref):
        self.inputs = np.array(inputs)
        self.ref_inputs = np.array(ref)

    def bump(self):
        if self.state != 'bumping' and self.state != 'shifting' and self.state != 'dead':
            self.state = 'bumping'
            self.speed = -SPEED*2
            self.rect[1] += self.speed 
            
    def shift(self):
        if self.state == 'running' and self.state != 'dead':
            self.state = 'shifting'

    def draw(self):
        screen.blit(self.image, self.rect)

class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.path.join(current_path, 'assets'), 'ground.png'))
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = x

    def update(self):
        self.rect[0] -= ground_speed
        self.rect[1] = GROUND_Y - 20

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x, is_big):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(cactus_path, 'big-cactus-1.png')).convert_alpha(),
            pygame.image.load(os.path.join(cactus_path, 'big-cactus-2.png')).convert_alpha(),
            pygame.image.load(os.path.join(cactus_path, 'big-cactus-3.png')).convert_alpha(),
            pygame.image.load(os.path.join(cactus_path, 'little-cactus-1.png')).convert_alpha(),
            pygame.image.load(os.path.join(cactus_path, 'little-cactus-2.png')).convert_alpha(),
            pygame.image.load(os.path.join(cactus_path, 'little-cactus-3.png')).convert_alpha(),
        ]

        self.image = self.images[random.randint(0, 2) if is_big else random.randint(3, 5)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = GROUND_Y - self.rect[3]
        self.h = GROUND_Y - self.rect[1]
    
    def update(self):
        self.rect[0] -= ground_speed

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, h):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(bird_path, 'bird1.png')).convert_alpha(),
            pygame.image.load(os.path.join(bird_path, 'bird2.png')).convert_alpha()
        ]

        self.time = 0
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = GROUND_Y - (self.rect[3] + h)
        self.h = h
    
    def update(self):
        if self.time % 3 == 0:
            self.current_image = (self.current_image + 1) % 2
            self.image = self.images[self.current_image]
        self.time += 1
        self.rect[0] -= ground_speed

def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]

def reset_game(randomic=False):
    global rex_group, generation_group, ground_group, obstacle_group, distance
    
    rex_group = start_population(Rex) if randomic else new_generation(generation_group, Rex)
    generation_group = pygame.sprite.Group()
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
            new_obstacle = Bird(OBSTACLE_GAP*2 + random.randint(-60, 60), random.randint(0, 2)*30) 
        else:
            new_obstacle = Cactus(OBSTACLE_GAP*2 + random.randint(-60, 60), random.randint(0, 1)) 
        obstacle_group.add(new_obstacle)

    count = 0
    best_rex = rex_group.sprites()[0]
    for rex in rex_group.sprites():
        get_senses(rex, obstacle_group, ground_speed)
        outputs = rex.feed_forward()
        
        rex.fitness = distance / 100

        if rex.rect[1] >= GROUND_Y - rex.rect[3]:
            rex.state = 'running'
        if not (outputs[0] > 0 and outputs[1] > 0):
            if outputs[0] > 0:
                rex.bump()
            if outputs[1] > 0:
                rex.shift() 

        if pygame.sprite.spritecollideany(rex, obstacle_group, pygame.sprite.collide_mask):
            generation_group.add(rex)
            rex_group.remove(rex)
        
        if count < PRINT_LIMIT:
            rex.draw()

        if rex.fitness >= best_rex.fitness:
            best_rex = rex

        count += 1

    texts = ['Distance to obstacle: ', 'Length (Obstacle): ', 'Width (Obstacle): ', 'Height (Obstacle): ', 'Velocity: ' ]
    delta_y = 2*NEURON_RADIUS + NEURON_GAP_Y
    for n in range(len(texts)):
        rect = display_text(screen, font, (40, 42 + n*delta_y), texts[n] + f'{best_rex.inputs[n]}', (0, 0, 0))
        if gap_neuron_text <= rect[2]:
            gap_neuron_text = rect[2]
    draw_neural_network(screen, best_rex, 40 + (gap_neuron_text+10) + NEURON_RADIUS, 50, 100, 10, 20)

    display_text(screen, font, (200, 10), f'Best Rex Neural Network', (0, 0, 0))
    display_text(screen, font, (500, 50 - NEURON_RADIUS), f'Generation: {generation}', (0, 0, 0))
    display_text(screen, font, (500, 50 - NEURON_RADIUS + 20), f'Distance: {distance}', (0, 0, 0))
    display_text(screen, font, (500, 50 - NEURON_RADIUS + 2*20), f'Highest distance: {highest_distance}', (0, 0, 0))
    
    if len(generation_group.sprites()) == POPULATION_LENGTH:
        reset_game()
        generation += 1
        ground_speed = 7
        

    rex_group.update()
    ground_group.update()
    obstacle_group.update()

    ground_group.draw(screen)
    obstacle_group.draw(screen)
    
    distance += 1
    if highest_distance <= distance:
        highest_distance = distance

    if distance % 1000 == 0 and ground_speed < 14:
        ground_speed += 1

    pygame.display.update()