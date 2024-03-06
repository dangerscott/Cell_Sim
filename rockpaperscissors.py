import pygame as py
import numpy
from CellClass import Cell, collide
from settings import enter_settings
import os

# Get the directory of the currently running Python script
current_directory = os.path.dirname(__file__)

#these are for calculating the nearest cell to a cell efficiently (important for telling if two cells have collided)
from BuildTree import build_ckd, find_nearest_cell

#heapq helps find top ten and bottom ten cells in terms of fitness
import heapq

#user's screen variables
from ScreenInfo  import screen_w, screen_h, screen_width_inches

screen_w = screen_w
screen_h = int(screen_h/1.1)

import random



import matplotlib.pyplot as plt

white = (200,200,200)
black = (0,0,0)



#Change initial parameters here
speed = 30
life_time = 1000
no_cells_in_gen = 10
size = 45

mutation_chance = 0.05

cells = []


for i in range(100):
    x,y = random.randrange(0,screen_w), random.randrange(0,screen_h)
    celli = Cell((x,y), size=size, speed = speed, strat = (1,0,0) )
    cells.append(celli)

pop = len(cells)

#
param_dict = {0:[speed, 100, 'Speed', 0], 1:[life_time, 5000, 'Lifetime (ms)', 0], 2:[no_cells_in_gen, len(cells)/2, 'No. cells per gen', 0],
                3:[size, 100, 'Size', 0], 4:[pop, 200, 'Population', 0], 5:[mutation_chance, 1, 'Mutation Chance', 3]}


#rps payoff matrix
rps = numpy.array([[0,-1,1],
                [1,0,-1],
                [-1,1,0]])

#play a game with payoff matrices
def engage(cella,cellb, payoffa, payoffb):
  
    row, col = numpy.random.choice([0,1,2], p=cella.strat), numpy.random.choice([0,1,2], p=cellb.strat)

    resulta, resultb = payoffa[row,col], payoffb[row,col]

    return resulta, resultb, row, col

font = py.font.Font(None, 36)
fontsmall = py.font.Font(None, 25)


#Initial popup
def popup():
    global current_directory
    py.init()
    w,h = 800,400
    screen = py.display.set_mode((w,h))
    py.display.set_caption('INFO')
    running = True
    text1 = 'This game simulates 3 species of Cell:'
    text2 = 'Rock, Paper, and Scissors.'
    text3 = 'They all play against eachother.'
    text4 = 'The luckiest cells are given fitness counters.'
    text5 = 'To pause, press spacebar. To quit, press q.'
    text6 = 'To access and exit settings, press s.'
    image = py.image.load(str(current_directory)+'/assets/rps.png')

    screen.fill((white))
    screen.blit(image, (0,0))
    py.image.load(str(current_directory)+'/assets/hawk_mouse.png')

    text1_surface = font.render(text1, True, black)
    text1_rect = text1_surface.get_rect(center = (w/2,h/2 - 170))
    screen.blit(text1_surface, text1_rect)

    text2_surface = font.render(text2, True, black)
    text2_rect = text2_surface.get_rect(center = (w/2,h/2 - 150))
    screen.blit(text2_surface, text2_rect)

    text3_surface = font.render(text3, True, black)
    text3_rect = text3_surface.get_rect(center = (w/2,h/2 - 130))
    screen.blit(text3_surface, text3_rect)

    text4_surface = font.render(text4, True, black)
    text4_rect = text4_surface.get_rect(center = (w/2,h/2 - 110))
    screen.blit(text4_surface, text4_rect)

    text5_surface = font.render(text5, True, black)
    text5_rect = text5_surface.get_rect(center = (w/2,h/2 -90))
    screen.blit(text5_surface, text5_rect)

    text6_surface = font.render(text6, True, black)
    text6_rect = text6_surface.get_rect(center = (w/2,h/2 -70))
    screen.blit(text6_surface, text6_rect)


    py.draw.rect(screen, black, (w/2-40, h-30-20, 80, 40))
    py.draw.rect(screen, (255,255,255), (w/2 -35, h-30-15, 70, 30))

    okrect = py.Rect(w/2 -40, h-50, 80, 40)


    text7_surace = font.render('OK', True, black)
    text_7_rect = text7_surace.get_rect(center = (w/2, h-30))
    screen.blit(text7_surace, text_7_rect)

    py.display.flip()
    while running == True:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_q:
                    running = False
            if event.type == py.MOUSEBUTTONDOWN:
                mouseposx, mouseposy = py.mouse.get_pos()
                mouserect = py.Rect(mouseposx, mouseposy, 1, 1)
                if mouserect.colliderect(okrect):
                    running = False




size = 60
fps = 60
font = py.font.Font(None, 36)
#Game loop
def run_cells(clock, overlay, screen, param_dict, cells):


    py.display.set_caption('Rock Paper Scissors')
    screen = py.display.set_mode((screen_w,screen_h))


    #The overlay that the graph sits over (Makes the cells less distracting when trying to read it)
    overlay.set_alpha(128)  # Set transparency (0 = fully transparent, 255 = fully opaque)
    overlay.fill(black)


    last_action_time = 0
    last_action_time1 = 0
    global average
    global fps
    global rps
    global font

    framecounter = 0
    avgstrat = (0,0,0)
    i=1
    y_data_fit = []
    x_data = []
    y_data_r = []
    y_data_p = []
    y_data_s = []

    framecounter = 0
    pause = 1
    running = True



    
    while running == True:

        speed = param_dict[0][0]
        life_time = param_dict[1][0]
        no_cells_in_gen = param_dict[2][0]
        size = param_dict[3][0]
        mutation_chance = param_dict[5][0]        
        #Build tree for cells to find nearest neighbour efficiently
        tree, list = build_ckd(cells)    

      # PRINT CELL CHARACTERISTICS ON CLICK
        for event in py.event.get():


            if event.type == py.QUIT:
                running = False

            if event.type == py.KEYDOWN and event.key == py.K_q:
                running = False
            
            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    pause = -pause

                #Enter settings on s
                if event.key == py.K_s:
                    param_dict = enter_settings(screen, param_dict)
                    speed = param_dict[0][0]
                    life_time = param_dict[1][0]
                    no_cells_in_gen = param_dict[2][0]
                    size = param_dict[3][0]
                    pop = param_dict[4][0]
                    mutation_chance = param_dict[5][0]
                
                    if param_dict[4][0] < len(cells)-5:
                        
                        deadlist = random.sample(cells, len(cells)-(param_dict[4][0]+2))
                        cells = [cell for cell in cells if cell not in deadlist]

                    if param_dict[4][0] > len(cells):
                        for i in range(param_dict[4][0] - len(cells)):
                            cells.append(Cell((random.random()*screen_w, random.random()*screen_h), 
                                             strat = random.choice(((0,0,1), (0,1,0), (1,0,0)))))
                    if param_dict[3][0] == 0:
                        param_dict[3][0] = 1
                    param_dict[2][1] = len(cells)/2    
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    mouse_pos = py.mouse.get_pos()

                    # Check if the mouse click is on a cell
                    for cell in cells:

                        # Define the bounding box around the cell
                        if numpy.linalg.norm(numpy.array(cell.position)-numpy.array(mouse_pos)) < cell.size/2:
                            print(cell)
                            break
        screen.fill(black)

        #draw cells
        for cell in cells:
            cell.size = param_dict[3][0]
            cell.speed = param_dict[0][0]
            py.draw.circle(screen, black, cell.position, (cell.size/2)+1)
            py.draw.circle(screen, cell.colour, cell.position, cell.size/2)
            if cell.disptime >= 1 and cell.disptime <= 10 and cell.age > 10:
                #Display what the cell played in its last game
                if cell.lastplayed == 0:
                    what_have_i_played = 'R'
                elif cell.lastplayed == 1:
                    what_have_i_played = 'P'
                else:
                    what_have_i_played = 'S'
                text_surface = py.font.Font(None, int((cell.size/100)*65)).render(what_have_i_played, True, black)

                text_rect = text_surface.get_rect()
                text_rect.center = (cell.position)

                # Draw text on the screen
                screen.blit(text_surface, text_rect)  
                        

        if pause == 1:
            for cell in cells:
                #this changes colour of cells based on strategy
                a,b,c = cell.strat
                cell.colour = (255*a, 255*b, 255*c)
                                
                #random movement

                if cell.pause >=10 or cell.pause == 0:
                    cell.position = cell.move.angle(cell.randangle) 
                    #if a cell has moved, update the tree
                    tree, list = build_ckd(cells)
                if framecounter%(fps*0.3) == 0:
                    #this is how the cell moves randomly
                    cell.randangle = (cell.randangle+random.choice([-1,1])*0.5)

                #this is the cell's nearest neighbour
                nearestCell = find_nearest_cell(tree, list, cell.position)

                #this is how the cell knows when to engage in a rps game
                if cell.pause == 0:
                    if collide(cell, nearestCell):
                        results = engage(cell, nearestCell, rps, -rps)
                        resulta = results[0]
                        resultb = results[1]
                        cell.lastplayed = results[2]
                        nearestCell.lastplayed = results[3]
                        cell.fitness += resulta
                        nearestCell.fitness += resultb

                        cell.disptime = 1
                        nearestCell.disptime = 1

                        #this makes it so cells can move away from eachother before playing                           
                        cell.pause = 1
                        nearestCell.pause = 1

                        



                if cell.pause >25:
                    cell.disptime = 0
                    cell.pause = 0
                if cell.pause >= 1:
                    cell.disptime +=1
                    cell.pause += 1
                cell.age +=1

            #reproduce and die every n milliseconds
            current_time = py.time.get_ticks()
            if current_time - last_action_time1 >= life_time:
                last_action_time1 = current_time 

                deadlist = []
                bornlist = []

                #let the ten cells with highest fitness reproduce:
                #bornlist is the top ten cells with highest fitness
                bornlist = heapq.nlargest(no_cells_in_gen, cells, key=lambda cell: cell.fitness)

                nbornlist = []
                for cell in bornlist:
                    nbornlist.append(Cell((cell.position), strat = cell.strat))

                bornlist = nbornlist

                #cells in bornlist are born with 0 fitness
                for baby in bornlist:

                    #for cell in bornlist, change its strategy slightly with a 5% chance
                    num = random.random()
                    if num > 1 - mutation_chance:


                        if baby.strat == (0,0,1):
                            baby.strat = (1,0,0)
                        elif baby.strat == (0,1,0):
                            baby.strat = (0,0,1)
                        elif baby.strat == (1,0,0):
                            baby.strat = (0,1,0)


                #deadlist is the bottom ten cells with the lowest fitness
                if param_dict[2][0] >= len(cells):
                    param_dict[2][0] = len(cells)
                deadlist = random.sample(cells, param_dict[2][0])

                for cell in bornlist:
                    # Create a new instance of the Cell class for the born cell
                    born_cell = Cell(position=cell.position, strat=cell.strat, size=size, speed=speed)
                    
                    # Reset the fitness of the born cell to zero
                    born_cell.fitness = 0
                    born_cell.pause = 10
                    # Append the born cell to the cells list
                    cells.append(born_cell)

                    avgstrat = avgstrat + numpy.array(cell.strat)
 

                cells = [cell for cell in cells if cell not in deadlist]


            current_time = py.time.get_ticks()
            

            screen.blit(overlay, (0,711))
            if current_time - last_action_time >= 2000 or last_action_time == 0:
                last_action_time = current_time                 
            # Append data for plotting
                
                x_data.append(framecounter)
                y_data_r.append(len([cell for cell in cells if cell.strat == (1,0,0)]))
                y_data_s.append(len([cell for cell in cells if cell.strat == (0,0,1)]))
                y_data_p.append(len([cell for cell in cells if cell.strat == (0,1,0)]))

                if y_data_r == []:
                    y_data_r.append(0)
                if y_data_s == []:
                    y_data_s.append(0)
                if y_data_p == []:
                    y_data_p.append(0)

                # Plot the data
                plt.gcf().set_alpha(0.0)
                plt.figure(figsize=(screen_width_inches, 3)) 

                plt.plot(x_data, y_data_r, color='red', linestyle='-')
                plt.plot(x_data, y_data_p, color='green',  linestyle='-')
                plt.plot(x_data, y_data_s, color='blue', linestyle='-')


                plt.ylim(0,len(cells))  # Set y-axis limits to 0.1 and 0.5
                if framecounter < 50000:
                    plt.xlim(0,50000)
                else:
                    plt.xlim(framecounter-50000, framecounter)
                plt.ylabel('Population', color = 'white')

                plt.grid(False)  # Turn off grid
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)
                plt.gca().spines['bottom'].set_visible(False)


                plt.gca().spines['left'].set_color('white')  # Set y-axis color to white
                plt.tick_params(axis='y', colors='white') 

                graphdir = str(current_directory) + '/assets/rpsgraph.png'
                plt.savefig(graphdir, bbox_inches='tight', pad_inches=0, transparent=True)  # Save the plot
                plt.close()

            # Load the graph image
                graph_image = py.image.load(graphdir)


            framecounter +=60

        i+=1

                    
        #print(graph_image.get_width())
        screen.blit(graph_image, (0, screen_h - graph_image.get_height() - 10))         
        clock.tick(fps)

        

        py.display.flip()

    py.quit()




def initialize_game():
    py.init()
    clock = py.time.Clock()
    overlay = py.Surface((1631, 711))
    overlay.set_alpha(128)
    overlay.fill(black)
    screen = py.display.set_mode((screen_w, screen_h))
    return clock, overlay, screen

def main():
    clock, overlay, screen = initialize_game()
    popup()
    run_cells(clock, overlay, screen, param_dict, cells)


if __name__ == "__main__":
    main()
