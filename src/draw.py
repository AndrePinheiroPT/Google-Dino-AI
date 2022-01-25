import pygame

def neural_network(screen, x, y, entitie):
    layer_gap = 100
    radius = 20
    # first layer
    for i in range(1, 6):
        input_color = (entitie.inputs[i-1]*255/1100, 0, 0)
        hidden_color = (255, 0, 0) if entitie.hidden[i-1] > 0 else (0, 0, 0)
        pygame.draw.circle(screen, input_color, (x + 50, y + 50*i), radius)
        pygame.draw.circle(screen, hidden_color, (x + 50 + layer_gap, y + 50*i), radius)
        for j in range(1, 6):  
            w_color = (255, 0, 0) if entitie.w1[i-1][j-1]*entitie.inputs[j-1] <= 0 else (200, 200, 200)
            pygame.draw.line(screen, w_color, (x + 50 + radius, y + 50*i), (x + 50 + layer_gap - radius, y + 50*j), 1)
        
    # secound layer
    for j in range(0, 2):
        outputs = entitie.feed_forward()
        output_color = (230, 0, 0) if outputs[j] > 0 else (0, 0, 0)
        pygame.draw.circle(screen, output_color, (x + 50 + 2*layer_gap, y + 100 + 50*j), radius)
        for i in range(1, 6):
            w_color = (255, 0, 0) if entitie.w2[j][i-1]*entitie.hidden[i-1] <= 0 else (200, 200, 200)
            pygame.draw.line(screen, w_color, (x + 50 + radius + layer_gap, y + 50*i), (x + 50 + 2*layer_gap - radius, y + 100 + 50*j), 1)