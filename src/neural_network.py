from main import Rex, ground_speed, obstacle_group

POPULATION_LENGTH = 2000

population = [ Rex(i) for i in range(0, POPULATION_LENGTH)]

for rex in population:
    for obstacle in obstacle_group.sprites():
        if rex.rect[0] <= obstacle.rect[0]:
            inputs = [obstacle.rect[0] - rex.rect[0], obstacle.rect[2], obstacle.rect[3], obstacle.h]
            rex.set_inputs(inputs)
            break
        else:
            continue
    