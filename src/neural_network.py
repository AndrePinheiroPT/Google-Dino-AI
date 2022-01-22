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
    group = population
    new_group = pygame.sprite.Group()
    
    for k in range(POPULATION_LENGTH):
        best = group.sprites()[0]
        for esp in group.sprites():
            esp.fitness = esp.dist / ref

            if best.fitness <= esp.fitness:
                best = esp
        
        group.remove(best)
        new_group.add(best)

    return new_group


def mutation(entitie):
    for i in range(4):
        rvalue = np.random.randint(-2000, 2001)/100
        if np.random.random() <= 0.05:
            if i == 0:
                entitie.w1[np.random.randint(5)][np.random.randint(5)] = rvalue
            elif i == 1:
                entitie.w2[np.random.randint(2)][np.random.randint(5)] = rvalue
            elif i == 2:
                entitie.b1[np.random.randint(5)] = rvalue
            elif i == 3:
                entitie.b2[np.random.randint(2)] = rvalue
    return entitie


def crossing_over(ent1, ent2, Esp):
    new_entitie = Esp()
    n1 = np.random.randint(5)
    new_entitie.w1[:n1] = ent1.w1[:n1]
    new_entitie.w1[n1:] = ent2.w1[n1:]

    n2 = np.random.randint(5)
    new_entitie.w2 = new_entitie.w2.transpose()
    new_entitie.w2[:n2] = ent1.w2.transpose()[:n2]
    new_entitie.w2[n2:] = ent2.w2.transpose()[n2:]
    new_entitie.w2 = new_entitie.w2.transpose()

    n3 = np.random.randint(5)
    new_entitie.b1[:n3] = ent1.b1[:n3]
    new_entitie.b1[n3:] = ent2.b1[n3:]

    n4 = np.random.randint(2)
    new_entitie.b2[:n4] = ent1.b2[:n4]
    new_entitie.b2[n4:] = ent2.b2[n4:]

    return new_entitie


def new_generation(population, ref, Especie):
    new_population = pygame.sprite.Group()
    population_fitness = fitness(population, ref)

    for i in range(0, POPULATION_LENGTH, 2):
        if i < POPULATION_LENGTH:
            prev_ent = Especie()
            prev_ent.w1 = population_fitness.sprites()[i].w1
            prev_ent.w2 = population_fitness.sprites()[i].w2
            prev_ent.b1 = population_fitness.sprites()[i].b1
            prev_ent.b2 = population_fitness.sprites()[i].b2

            new_population.add(prev_ent)

        try:
            new_ent = crossing_over(population_fitness.sprites()[i], population_fitness.sprites()[i+1], Especie)
            new_population.add(mutation(new_ent))
        except Exception:
            pass

    return new_population