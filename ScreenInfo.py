
#This is general screen stuff (colours and screen dimensions)
white = (255, 255, 255)
import pygame as py
import screeninfo
py.init()
# Get display info
display_info = py.display.Info()
# Get actual screen width and height
screen_w = display_info.current_w
screen_h = display_info.current_h 


import tkinter as tk

def get_screen_width_in_inches():
    monitors = screeninfo.get_monitors()
    primary_monitor = monitors[0]  # Assuming you want the primary monitor
    width_mm = primary_monitor.width_mm
    width_inches = width_mm / 25.4
    return width_inches

screen_width_inches = get_screen_width_in_inches()
