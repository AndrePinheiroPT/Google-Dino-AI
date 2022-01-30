import pygame

def initial_neuron(mp_y, array, delta_y, gap_y, radius):
    if len(array) % 2 == 0:
        return round(mp_y - (gap_y/2 + radius + (len(array)-2)*delta_y))
    elif len(array) == 1:
        return round(mp_y)
    elif len(array) % 2 != 0:
        return round(mp_y - (len(array)/2 - 1/2)*delta_y)


def draw_neural_network(screen, entitie, x, y, gap_x, gap_y, radius):
    delta_y = 2*radius + gap_y
    my = y + (len(entitie.inputs) - 1)*delta_y/2
    outputs = entitie.feed_forward()
    hidden_init = initial_neuron(my, entitie.hidden, delta_y, gap_y, radius)
    output_init = initial_neuron(my, outputs, delta_y, gap_y, radius)

    # first layer
    for n in range(len(entitie.inputs)):
        i_y = y + n*delta_y
        input_color = (round(255*abs(entitie.inputs[n])/entitie.ref_inputs[n]), 0, 0)
        
        pygame.draw.circle(screen, input_color, (x, i_y), radius)

        for k in range(len(entitie.hidden)):
            
            hidden_color = (255, 0, 0) if entitie.hidden[k] > 0 else (0, 0, 0)
            pygame.draw.circle(screen, hidden_color, (x + gap_x, hidden_init + k*delta_y), radius)


            w_color = (255, 0, 0) if entitie.w1[n][k]*entitie.inputs[k] <= 0 else (200, 200, 200)
            pygame.draw.line(screen, w_color, (x + radius, i_y), (x + gap_x - radius, hidden_init + k*delta_y), 1)
        
    # secound layer
    for j in range(0, 2):
        
        output_color = (255, 0, 0) if outputs[j] > 0 else (0, 0, 0)
        pygame.draw.circle(screen, output_color, (x + 2*gap_x, output_init + j*delta_y), radius)
        for i in range(len(entitie.hidden)):
            w_color = (255, 0, 0) if entitie.w2[j][i]*entitie.hidden[i] <= 0 else (200, 200, 200)
            pygame.draw.line(screen, w_color, (x + gap_x + radius, hidden_init + i*delta_y), (x + 2*gap_x - radius, output_init + j*delta_y), 1)


def display_text(screen, font, coords, txt, color):
    textsurface = font.render(txt, False, color)
    screen.blit(textsurface, coords)
    return textsurface.get_rect()