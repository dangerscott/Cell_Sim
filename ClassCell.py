#This is where the Cell class is kept. It also contains the movement logic for the cells

import random
from screenstuff import screen_w, screen_h, white

import numpy

import math


class Cell:
    def __init__(self, position, strat = numpy.random.dirichlet(numpy.ones(3)), fitness=0, speed = 10, age = 0, colour = white, size=5, isdead=0, ishawk = 1):

        if position is None:
            position = (random.randint(0,screen_w), random.randint(0,screen_h))

        self.position = position
        self.disptime = 0 
        self.lastplayed = 0

        self.move = self.move(self)

        self.ishawk = ishawk

        self.randangle = 2*math.pi*random.random()
        self.size = size

        self.pause = 0

        self.fitness = 0

        self.angle = 0

        self.strat = strat

        self.colour = colour
                
        #This says a cell's colour is dependent on its strategy.         
        # if self.ishawk == 1:
        #     self.colour = (0,255,0)
        # else:
        #     self.colour = (255,0,0)


        self.speed = speed
        self.isdead = isdead

    
    def __str__(self):
        return f"Position: {self.position}, Fitness: {self.fitness}, Strategy: {self.strat}, speed: {self.speed}, randangle: {self.randangle}"


    class move:
        def __init__(self, cell):
            self.cell = cell
        
        def angle(self, theta):
            step = self.cell.speed

            

            x, y = self.cell.position

            dx = ((numpy.radians(numpy.cos(theta))))*5*step 
            dy = ((numpy.radians(numpy.sin(theta))))*5*step

            if numpy.linalg.norm((dx, dy)) > self.cell.speed:
                # Scale down dx and dy to ensure the distance doesn't exceed the maximum allowed
                scaling_factor = self.cell.speed / numpy.linalg.norm((dx, dy))
                dx *= scaling_factor
                dy *= scaling_factor

            self.cell.position = ((x+dx)%screen_w, (y-dy)%screen_h)

            #self.cell.angle = theta

            return self.cell.position

def collide(a,b):
    posa = numpy.array(a.position)
    posb = numpy.array(b.position)
    distance = numpy.linalg.norm(posb-posa)



    try:
        b.size
        if distance < a.size/2 + b.size/2:
            return True
    except AttributeError:
        if distance < a.size/2 + 1:
            return True


