import pygame as py
from screenstuff import screen_w, screen_h
import numpy as np

def slider(screen, running, corner, parameter, parameter_max, parameter_name):
    
    smallfont = py.font.Font(None, 25)
    bigfont = py.font.Font(None, 36)
    x,y = corner
    wx, wy = x+5, y+5
    gx, gy = wx+20, wy+20



    parameter_length = 160*(parameter/parameter_max)
    slider_coords = (gx+parameter_length, gy+5)

    slider_running = True
    settings_running = True
    dragging = False
    while settings_running == True:
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = py.mouse.get_pos()
                if np.linalg.norm(np.array((mouse_x, mouse_y)) - np.array(slider_coords)) <= 10:
                    dragging = True
            if event.type == py.MOUSEBUTTONUP and event.button == 1:
                    dragging = not dragging
            if event.type == py.MOUSEMOTION:
                if dragging:
                    mouse_x = py.mouse.get_pos()[0]
                    if mouse_x >= gx+160:
                        mouse_x = gx+160
                    if mouse_x <= gx:
                        mouse_x = gx
                    
                    slider_coords = (mouse_x, gy+5)
            if event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    settings_running = False
                elif event.key == py.K_q:
                    settings_running = False
                    running = False
          
        py.draw.rect(screen, (0,0,0), (x, y, 210, 60)) #Black Border
        py.draw.rect(screen, (255,255,255), (wx, wy, 200, 50)) #White area


        py.draw.rect(screen, (128, 128, 128), (gx, gy, 160, 10)) #Grey slider rect

        py.draw.circle(screen, (128,128,128), (gx-2, gy+5), 5)
        py.draw.circle(screen, (128,128,128), (gx+160+2, gy+5), 5) #Rounded edges for slider rect

        py.draw.circle(screen, (0,0,0), (slider_coords), 10)

        #Name of slider
        slider_name = smallfont.render(str(parameter_name), True, (0,0,0))
        name_rect = slider_name.get_rect()
        name_rect.center = (wx + 100, wy + 10)
        screen.blit(slider_name, name_rect)

        #Slider value
        slider_value = round(((slider_coords[0] - gx)/160)*parameter_max, 3)
        new_parameter = slider_value
        slider_value = bigfont.render(str(slider_value), True, (0,0,0))
        value_rect = slider_value.get_rect()
        value_rect.center = (wx + 100, wy+40)
        screen.blit(slider_value, value_rect)





        py.display.flip()
    
    return running, new_parameter

