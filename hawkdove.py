#################################################
#when you run this file, it should Just Work. Hawks are red, doves are green.
#If you press spacebar, the game pauses. If you press


import pygame as py
import numpy
from settings import enter_settings

from CellClass import Cell, collide
import tkinter as tk

import matplotlib.pyplot as plt

import os

# Get the directory of the currently running Python script
current_directory = os.path.dirname(__file__)


#these are for calculating the nearest cell to a cell efficiently (important for telling if two cells have collided)
from BuildTree import build_ckd, find_nearest_cell

#heapq helps find top ten and bottom ten cells in terms of fitness
import heapq

#user's screen variables
from ScreenInfo import screen_w, screen_h, screen_width_inches
#TO ADJUST GAME SIZE, MULTIPLY THESE BY YOUR DESIRED NUMBER
screen_w = screen_w
screen_h = screen_h
size = 20
import random

white = (200,200,200)
black = (0,0,0)
counter = 0





speed = 40

def generate_population(ishawk, n):
    population = []
    if ishawk == 0.5:
        for _ in range(n):
            x, y = random.randrange(0, screen_w), random.randrange(0, screen_h)
            celli = Cell((x, y), size=size , speed=speed, ishawk = random.choice((-1,1)))
            population.append(celli)
    else:
        for _ in range(n):
            x, y = random.randrange(0, screen_w), random.randrange(0, screen_h)
            celli = Cell((x, y), size=size , speed=speed, ishawk = ishawk)
            population.append(celli)
    return population



#hawk, dove payoff matrix
playera = numpy.array([[0,3],
                       [1,2]])
playerb = numpy.array([[0,1],
                       [3,2]])


def hawk_dove(cella,cellb):
    if cella.ishawk == 1:
        row = 0
    else:
        row = 1
    if cellb.ishawk == 1:
        col  = 0
    else:
        col = 1

    return(playera[row, col], playerb[row,col])

fps = 30
font = py.font.Font(None, 36)
fontsmall = py.font.Font(None, 25)

def popup():
    global current_directory
    py.init()
    w,h = 800,400
    screen = py.display.set_mode((w,h))
    py.display.set_caption('INFO')
    running = True
    text1 = 'This game simulates Hawks and Doves interacting.'
    text2 = 'Hawks are red, Doves are green.'
    text3 = 'To pause/unpause, press spacebar.'
    text4 = 'There are three iterations of different populations.'
    text5 = 'To cycle through them, press q. To access/exit settings, press s.'
    image = py.image.load(str(current_directory)+'/assets/hawk_mouse.png')

    screen.fill((white))
    screen.blit(image, (0,0))
    py.image.load(str(current_directory)+'/assets/hawk_mouse.png')

    text1_surface = font.render(text1, True, black)
    text1_rect = text1_surface.get_rect(center = (w/2,h/2 - 180))
    screen.blit(text1_surface, text1_rect)

    text2_surface = font.render(text2, True, black)
    text2_rect = text2_surface.get_rect(center = (w/2,h/2 - 160))
    screen.blit(text2_surface, text2_rect)

    text3_surface = font.render(text3, True, black)
    text3_rect = text3_surface.get_rect(center = (w/2,h/2 - 140))
    screen.blit(text3_surface, text3_rect)

    text4_surface = font.render(text4, True, black)
    text4_rect = text4_surface.get_rect(center = (w/2,h/2 -120))
    screen.blit(text4_surface, text4_rect)

    text5_surface = font.render(text5, True, black)
    text5_rect = text5_surface.get_rect(center = (w/2,h/2 - 100))
    screen.blit(text5_surface, text5_rect)


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

 
    py.quit()
#Game loop
def run_cells(ishawk, n):
    cells = generate_population(ishawk, n)
    py.init()
    clock = py.time.Clock()


    screen = py.display.set_mode((screen_w, screen_h))
    py.display.set_caption('Hawks and Doves')
    overlay = py.Surface((1631, 711))
    overlay.set_alpha(128)
    overlay.fill(black)



    global average
    global fps
    global rps

    x_data = []
    y_data_h = []
    y_data_d = []

    running = True

    framecounter = 0

    last_action_time3 = 0
    framecounter = 0
    pause = True
    #Build tree for cells to find nearest neighbour efficiently
    tree, list = build_ckd(cells)    
    last_action_time1, last_action_time2 = py.time.get_ticks(), py.time.get_ticks()

    mutation_chance = 0.05
    speed = 55
    life_time = 1000
    no_cells_in_gen = 10
    size = 15
    pop = len(cells)

    param_dict = {0:[speed, 100, 'Speed', 0], 1:[life_time, 5000, 'Reprod. interval (ms)', 0], 2:[no_cells_in_gen, len(cells)/2, 'Cells born/dead per gen', 0],
                  3:[size, 100, 'Size', 1], 4:[pop, 500, 'Population', 0], 5:[mutation_chance, 1, 'Mutation Chance', 3]}
    

    while running == True:


      # PRINT CELL CHARACTERISTICS ON CLICK
        for event in py.event.get():


            if event.type == py.QUIT:
                running = False

            if event.type == py.KEYDOWN and event.key == py.K_q:
                running = False
            
            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    pause = not pause
                if event.key == py.K_s:
                    param_dict = enter_settings(screen, param_dict)
                    if param_dict[4][0] < len(cells)-5:
                        
                        deadlist = random.sample(cells, len(cells)-(param_dict[4][0]+2))
                        cells = [cell for cell in cells if cell not in deadlist]
                        deadlist =[]

                    if param_dict[4][0] > len(cells):
                        for i in range(param_dict[4][0] - len(cells)):
                            cells.append(Cell((random.random()*screen_w, random.random()*screen_h), ishawk = random.choice((-1,1))))


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



        if pause:
            for cell in cells:                  
                #random movement
                if  cell.pause == 0 or cell.pause > 1:
                    cell.move.angle(cell.randangle) 

                    #if a cell has moved, update the tree
                    tree, list = build_ckd(cells)
                cell.randangle = cell.randangle+(random.choice([-1,1])*0.2)

                #this is the cell's nearest neighbour
                nearestCell = find_nearest_cell(tree, list, cell.position)

                #this is how the cell knows when to engage in a rps game
                if cell.pause == 0:
                    if collide(cell, nearestCell):
                        resulta, resultb = hawk_dove(cell, nearestCell)
                        cell.fitness += resulta
                        nearestCell.fitness += resultb

                        #this makes it so cells can move away from eachother before playing                           
                        cell.pause = 1
                        nearestCell.pause = 1

                        



                if cell.pause >50:
                    cell.pause = 0
                if cell.pause >= 1:
                    cell.pause += 1
 

            #reproduce and die every 5 secs

            current_time = py.time.get_ticks()
            if current_time - last_action_time1 >= param_dict[1][0]:  # Convert seconds to milliseconds
                last_action_time1 = current_time 

                #let the n cells with highest fitness reproduce:

                if param_dict[2][0] > len(cells):
                    param_dict[2][0] = len(cells)

                bornlist = heapq.nlargest(param_dict[2][0], cells, key=lambda cell: cell.fitness)

                nbornlist = []
                for cell in bornlist:
                    nbornlist.append(Cell((cell.position), cell.ishawk))
                bornlist = []

                #cells in bornlist are born with 0 fitness
                for cell in nbornlist:
                    cell.randangle = random.uniform(0, 2 * numpy.pi)
                    cell.fitness = 0
                    cell.pause = 1
                    cell.speed = param_dict[0][1]

                    # Mutate the cell based on the mutation chance
                    if random.random() < param_dict[5][0]:
                        cell.ishawk *= -1

                #deadlist is n random cells
                if param_dict[2][0] >= len(cells):
                    param_dict[2][0] = len(cells)
                deadlist = random.sample(cells, param_dict[2][0])
                cells = [cell for cell in cells if cell not in deadlist]

                for cell in nbornlist:
                    cells.append(cell)


            #graph stuff
            current_time = py.time.get_ticks()
            if current_time - last_action_time3 >= 1000 or last_action_time3 == 0:  # Convert seconds to milliseconds
                last_action_time3 = current_time           

                x_data.append(framecounter)
                y_data_h.append(len([cell for cell in cells if cell.ishawk == 1]))
                y_data_d.append(len([cell for cell in cells if cell.ishawk == -1]))
                    
                # Plot the data
                plt.figure(figsize=(screen_width_inches, 3)) 
                try:
                    plt.plot(x_data, y_data_h, color='red', linestyle='-', markeredgecolor='black', markeredgewidth=1)
                except:
                    pass

                #print(x_data, y_data_d)
                try:
                    plt.plot(x_data, y_data_d, color='green',  linestyle='-', markeredgecolor='black', markeredgewidth=1)
                except:
                    pass
                
                plt.ylim(0, len(cells))  # Set y-axis limit to population

                # Set x-axis limit dynamically
                if framecounter < 50:
                    plt.xlim(0,50)
                else:
                    plt.xlim(framecounter-50, framecounter)

                plt.grid(False)  # Turn off grid
                plt.ylabel('Population', color = 'white')
                plt.tick_params(axis='y', colors='white')  # Set tick color to white for y-axis

                graphdir = str(current_directory) + '/assets/graph_hawkdove.png'
                plt.savefig(graphdir, bbox_inches='tight', pad_inches=0, transparent=True)  # Save the plot
                plt.close()
                framecounter += 1
          

        #draw cells
        for cell in cells:
            if cell.ishawk == -1:
                cell.colour = (0,255,0)
            elif cell.ishawk == 1 :
                cell.colour = (255,0,0)
                    
            cell.size = param_dict[3][0]
            cell.speed = param_dict[0][0]
            py.draw.circle(screen, black, cell.position, (cell.size)+1)
            py.draw.circle(screen, cell.colour, cell.position, cell.size)
        try:
            graph_image = py.image.load(graphdir)
            screen.blit(overlay, (0,711))
            screen.blit(graph_image, (0, screen_h - graph_image.get_height() - 60)) 
        except:
            pass   
        




        py.display.flip()
    py.quit()

popup()
run_cells(0.5, 100)
run_cells(1, 100)
run_cells(-1, 100)
