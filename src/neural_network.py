import pygame
import numpy as np
POPULATION_LENGTH = 5000

def start_population(Especie):
    especie_group = pygame.sprite.Group()
    for i in range(0, POPULATION_LENGTH):
        especie_group.add(Especie())

    return especie_group

def get_senses(entitie, obstacles_group, velocity):
    for obstacle in obstacles_group.sprites():
        # distance between rex and obstacle, obstacle witdth, obstacle height, obstacle distance to the ground
        inputs = [obstacle.rect[0] - entitie.rect[0], obstacle.rect[2], obstacle.rect[3], obstacle.h, velocity]
        entitie.set_inputs(inputs)
        break

def relu(x):
    return np.maximum(x, 0)

def sort_fitness(population):
    group = population.copy()
    new_group = pygame.sprite.Group()
    
    for k in range(len(group.sprites())):
        best = group.sprites()[0]
        for esp in group.sprites():
            if best.fitness <= esp.fitness:
                best = esp
        
        group.remove(best)
        new_group.add(best)

    return new_group


def mutation(entitie):
    for i in range(4):
        rvalue = np.random.randint(-1000, 1001)
        if np.random.random() <= 0.1:
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


def new_generation(population, Especie):
    new_population = pygame.sprite.Group()
    sort_entities = sort_fitness(population.copy())

    for i in range(0, POPULATION_LENGTH, 2):
        if i < POPULATION_LENGTH:
            prev_ent = Especie()
            prev_ent.w1 = sort_entities.sprites()[i].w1
            prev_ent.w2 = sort_entities.sprites()[i].w2
            prev_ent.b1 = sort_entities.sprites()[i].b1
            prev_ent.b2 = sort_entities.sprites()[i].b2

            new_population.add(mutation(prev_ent))
        try:
            new_ent = crossing_over(sort_entities.sprites()[i], sort_entities.sprites()[i+1], Especie)
            new_population.add(mutation(new_ent))
        except Exception:
            pass

    return new_population
