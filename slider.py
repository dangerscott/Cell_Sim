import pygame as py
from screenstuff import screen_w, screen_h
import numpy as np


class Slider:
    def __init__(self, param_value, param_max, param_name, center_coords):
        self.center = center_coords
        self.name = param_name
        self.max = param_max
        self.value = param_value
        



def gensliders(param_dict):
    sliders = []
    n=0
    for i in param_dict:        
        value,max,name,sigfig = param_dict[i]

        parameter_length = 160*(value/max)
        slider_coords = ((screen_w/2)+25+parameter_length, (i*60)+30)

        sliders.append(Slider(value, max, name, slider_coords))

    return(sliders)

def draw_boxes(screen, sliders, param_dict):
    smallfont = py.font.Font(None, 25)
    bigfont = py.font.Font(None, 36)
    for slider in sliders:


        corner = screen_w/2, (slider.center[1]-30)
        x,y = corner
        wx, wy = x+5, y+5
        gx, gy = wx+20, wy+20
        py.draw.rect(screen, (0,0,0), (x, y, 210, 60)) #Black Border
        py.draw.rect(screen, (255,255,255), (wx, wy, 200, 50)) #White area


        py.draw.rect(screen, (128, 128, 128), (gx, gy, 160, 10)) #Grey slider rect

        py.draw.circle(screen, (128,128,128), (gx-2, gy+5), 5)
        py.draw.circle(screen, (128,128,128), (gx+160+2, gy+5), 5) #Rounded edges for slider rect

        slider_name = smallfont.render(str(slider.name), True, (0,0,0))
        name_rect = slider_name.get_rect()
        name_rect.center = (wx + 100, wy + 10)
        screen.blit(slider_name, name_rect)
    
        slider_value = slider.center[0]
        slider_value -= ((screen_w/2)+25)
        slider_value /= 160
        slider_value *= slider.max
        




        sigfig = param_dict[sliders.index(slider)][3]
        slider_value = round(slider_value, sigfig)
        if sigfig == 0 :
            slider_value = int(slider_value)
        param_dict[sliders.index(slider)][0] = slider_value
        slider_value = bigfont.render(str(slider_value), True, (0,0,0))
        value_rect = slider_value.get_rect()
        value_rect.center = (screen_w/2 + 100, sliders.index(slider)*60+45)
        screen.blit(slider_value, value_rect)
        py.draw.circle(screen, (0,0,0), (slider.center), 10)

    return param_dict

#This sits inside a while dragging loop, where you should already have determined which slider you want to drag
def move_sliders(screen, slider, mouse_pos):
    mouse_x, mouse_y = mouse_pos

    if mouse_x < (screen_w/2)+25:
        mouse_x = (screen_w/2)+25
    if mouse_x > (screen_w/2)+160+25:
        mouse_x = (screen_w/2)+160+25
    
    oldx,y  = slider.center
    oldx = mouse_x

    slider.center = (oldx, y)

        

def enter_settings(screen, param_dict):
    sliders= gensliders(param_dict)
    settings = True
    while settings == True:
    #Find out where the mouse is clicking :)
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    settings = False
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = py.mouse.get_pos()
                for slider in sliders:
                    if mouse_pos[1] < slider.center[1]+30:
                        if mouse_pos[1] > slider.center[1]-30:
                            whichslider = sliders.index(slider)
                try:
                    move_sliders(screen, sliders[whichslider], (mouse_pos))
                except:
                    pass

        param_dict = draw_boxes(screen, sliders, param_dict)

        py.display.flip()

    return param_dict



