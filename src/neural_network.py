import pygame
import numpy as np
POPULATION_LENGTH = 100

def start_population(Especie):
    especie_group = pygame.sprite.Group()
    for i in range(0, POPULATION_LENGTH):
        especie_group.add(Especie(i))

    return especie_group

def get_senses(especie_group, obstacles_group, args):
    for especie in especie_group.sprites():
        for obstacle in obstacles_group.sprites():
            if especie.rect[0] <= obstacle.rect[0]:
                # distance between rex and obstacle, obstacle witdth, obstacle height, obstacle distance to the ground
                inputs = [obstacle.rect[0] - especie.rect[0], obstacle.rect[2], obstacle.rect[3], obstacle.h, *args]
                especie.set_inputs(inputs)
                break
            else:
                continue

def relu(x):
    return np.maximum(x, 0)

def fitness(population, ref):
    dist_list = []
    for esp in population:
        dist_list.append(esp.dist / ref)
    return dist_list

def crossing_over(best_couple, Especie):
    new_genome = Especie(0)
    i = np.random.randint(5)

    tmp = best_couple[0].weights_layer1[:i].copy()
    #self.weights_layer1 = np.random.randint(-10, 11, size=(5, 5)) / 10
        #self.bias_layer1 = np.random.randint(-10, 11, size=(5, 1)) / 10

        #self.weights_layer2 = np.random.randint(-10, 11, size=(2, 5)) / 10
        #self.bias_layer2 = np.random.randint(-10, 11, size=(2, 1)) / 10
    
    best_couple[0]
    new_genome.weights_layer1 = 


def mutation(genome):


def new_generation(population, ref, Especie):
    population_fitness = fitness(population, ref)

    best_couple = pygame.sprite.Group()

    for id in range(0, POPULATION_LENGTH):
        if np.random.random() >= population_fitness[id]:
            best_couple.add(population[id])
        
        if len(best_couple) >= 2:
            break
    
    crossing_over(best_couple, esp)

    if np.random.random() <= 0.1:
        mutatuion()
    return population