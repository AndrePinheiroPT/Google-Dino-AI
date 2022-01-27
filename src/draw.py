import pygame

def draw_neural_network(screen, entitie, x, y, gap_x=100, gap_y=20, radius=20):
    # first layer
    for n in range(len(entitie.inputs)):
        delta_y = 2*radius + gap_y
        i_y = y + n*delta_y

        my = y + (len(entitie.inputs) - 1)*delta_y/2

        input_color = (255, 0, 0)
        
        pygame.draw.circle(screen, input_color, (x, i_y), radius)

        for k in range(len(entitie.hidden)):
            if len(entitie.hidden) % 2 == 0:
                a = my - (gap_y/2 + radius + (len(entitie.hidden)-2)*delta_y)
            elif len(entitie.hidden) == 1:
                a = my 
            elif len(entitie.hidden) % 2 != 0:
                a = my - (len(entitie.hidden)-3)*delta_y

            hidden_color = (255, 0, 0) if entitie.hidden[k] > 0 else (0, 0, 0)
            pygame.draw.circle(screen, hidden_color, (x + gap_x, round(a) + k*delta_y), radius)


            w_color = (255, 0, 0) if entitie.w1[n][k]*entitie.inputs[k] <= 0 else (200, 200, 200)
            pygame.draw.line(screen, w_color, (x + radius, i_y), (x + gap_x - radius, round(a) + k*delta_y), 1)
        
    # secound layer
    #for j in range(0, 2):
        #outputs = entitie.feed_forward()
        #output_color = (230, 0, 0) if outputs[j] > 0 else (0, 0, 0)
        #pygame.draw.circle(screen, output_color, (x + 50 + 2*layer_gap, y + 100 + 50*j), radius)
        #for i in range(1, 6):
           # w_color = (255, 0, 0) if entitie.w2[j][i-1]*entitie.hidden[i-1] <= 0 else (200, 200, 200)
            #pygame.draw.line(screen, w_color, (x + 50 + radius + layer_gap, y + 50*i), (x + 50 + 2*layer_gap - radius, y + 100 + 50*j), 1)