from hmac import new
import pygame
import numpy as np
POPULATION_LENGTH = 100

def start_population(Especie):
    especie_group = pygame.sprite.Group()
    for i in range(0, POPULATION_LENGTH):
        especie_group.add(Especie())

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
    for esp in population.sprites():
        dist_list.append(esp.dist / ref)
    return dist_list

def mutation(entitie):
    if np.random.random() <= 0.1:
        entitie.weights_layer1[np.random.randint(5)][np.random.randint(5)] = np.random.randint(-10, 11)/10
    if np.random.random() <= 0.1:
        entitie.weights_layer2[np.random.randint(2)][np.random.randint(5)] = np.random.randint(-10, 11)/10
    if np.random.random() <= 0.1:
        entitie.bias_layer1[np.random.randint(5)] = np.random.randint(-10, 11)/10
    if np.random.random() <= 0.1:
        entitie.bias_layer2[np.random.randint(2)] = np.random.randint(-10, 11)/10
    return entitie


def new_generation(population, ref, Especie):
    population_fitness = fitness(population, ref)

    best_id = 0
    for i in range(1, POPULATION_LENGTH):
        if population_fitness[best_id] <= population_fitness[i]:
            best_id = i

    best_entitie = population.sprites()[best_id]

    new_population = pygame.sprite.Group()

    for i in range(0, 100):
        new_entitie = Especie()
        new_entitie.weights_layer1 = best_entitie.weights_layer1 
        new_entitie.bias_layer1 = best_entitie.bias_layer1 
        new_entitie.weights_layer2 = best_entitie.weights_layer2
        new_entitie.bias_layer2 = best_entitie.bias_layer2
        new_entitie = mutation(new_entitie)
        new_population.add(new_entitie)

    return new_population