#################################################
#when you run this file, it should Just Work. Hawks are red, doves are green.
#If you press spacebar, the game pauses. If you press


import pygame as py
import numpy
from slider import slider

from ClassCell import Cell, collide
import tkinter as tk

import matplotlib.pyplot as plt

import os

# Get the directory of the currently running Python script
current_directory = os.path.dirname(__file__)


#these are for calculating the nearest cell to a cell efficiently (important for telling if two cells have collided)
from treestuff import build_ckd, find_nearest_cell

#heapq helps find top ten and bottom ten cells in terms of fitness
import heapq

#user's screen variables
from screenstuff import screen_w, screen_h, screen_width_inches
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
    while running == True:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_q:
                    running = False
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
        py.display.flip()
 
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
    mutation_chance = 0.05
    framecounter = 0
    pause = True
    #Build tree for cells to find nearest neighbour efficiently
    tree, list = build_ckd(cells)    
    last_action_time1, last_action_time2 = py.time.get_ticks(), py.time.get_ticks()
    speed = 40
    life_time = 1000
    no_cells_in_gen = 10
    size = 20
    pop = 200
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
                    running, mutation_chance = slider(screen, running, (screen_w-210, 0), mutation_chance, 1, 'Chance of mutation')
                    running, speed = slider(screen, running, (screen_w -210, 60), speed, 100, 'Cell speed')
                    running, size = slider(screen, running, (screen_w-210, 120), size, 100, 'Cell radius')

                    life_time = life_time/1000
                    running, life_time = slider(screen, running, (screen_w - 210, 180), life_time, 100, 'Cell lifespan (s)')
                    life_time = life_time*1000

                    running, no_cells_in_gen = slider(screen, running, (screen_w - 210, 240), no_cells_in_gen, 50, 'Cells born/dead / gen')

                    no_cells_in_gen = int(no_cells_in_gen)

                    running, pop = slider(screen, running, (screen_w-210, 300), pop, 500, "Population")
                    pop = int(pop)
                    if pop < 10:
                        pop = 10
                        deadlist = random.sample(cells, len(cells)-pop)
                        cells = [cell for cell in cells if cell not in deadlist]
                    elif len(cells) > pop:
                        deadlist = random.sample(cells, len(cells)-pop)
                        cells = [cell for cell in cells if cell not in deadlist]

                    if len(cells)+1  < pop:
                        newcells = generate_population(ishawk, pop-len(cells))
                        for cell in newcells:
                            cells.append(cell)
                    
                    for cell in cells:
                        cell.size = size
                        cell.speed = speed                    

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

                current_time = py.time.get_ticks()

                if current_time - last_action_time2 >= 1:
                    last_action_time2 = current_time
                    #this is how the cell moves randomly
                    cell.randangle = (cell.randangle+random.choice([-1,1])*0.5)

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
            if current_time - last_action_time1 >= life_time:  # Convert seconds to milliseconds
                last_action_time1 = current_time

                deadlist = []
                bornlist = []

                #let the fifty cells with highest fitness reproduce:
                #bornlist is the top ten cells with highest fitness
                if no_cells_in_gen > len(cells):
                    no_cells_in_gen = len(cells)
                bornlist = heapq.nlargest(no_cells_in_gen, cells, key=lambda cell: cell.fitness)

                #cells in bornlist are born with 0 fitness
                for cell in bornlist:
                    cell.randangle = random.uniform(0, 2 * numpy.pi)
                    cell.fitness = 0
                    cell.pause = 1
                    cell.speed = speed

                    #for cell in bornlist, change it to hawk/dove with a 5% chance
                    if random.random() > 1 - mutation_chance:
                        cell.ishawk = cell.ishawk*-1


                #deadlist is n random cells

                deadlist = random.sample(cells, no_cells_in_gen)


                for cell in bornlist:
                    cells.append(Cell((cell.position), ishawk = cell.ishawk, size = size))
                cells = [cell for cell in cells if cell not in deadlist]

                
     
                
        


            current_time = py.time.get_ticks()
            if current_time - last_action_time3 >= 1000 or last_action_time3 == 0:  # Convert seconds to milliseconds
                last_action_time3 = current_time           

                x_data.append(framecounter)
                y_data_h.append(len([cell for cell in cells if cell.ishawk == 1]))
                y_data_d.append(len([cell for cell in cells if cell.ishawk == -1]))


                h_list = []
                d_list = []
                for cell in cells:
                    if cell.ishawk == 1:
                        h_list.append(cell)
                    else:
                        d_list.append(cell)
                    


            

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
            else:
                cell.colour = (255,0,0)
            py.draw.circle(screen, black, cell.position, (cell.size/2)+1)
            py.draw.circle(screen, cell.colour, cell.position, cell.size/2)
        try:
            graph_image = py.image.load(graphdir)
            screen.blit(overlay, (0,711))
            screen.blit(graph_image, (0, screen_h - graph_image.get_height() - 60)) 
        except:
            pass   
        




        py.display.flip()
    py.quit()

#Mutation chance slider
    

popup()
run_cells(0.5, 200)
run_cells(1, 200)
run_cells(-1, 200)
