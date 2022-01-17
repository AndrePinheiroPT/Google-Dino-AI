import pygame
POPULATION_LENGTH = 1

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
    