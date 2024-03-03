
#This is general screen stuff (colours and screen dimensions)
white = (255, 255, 255)
import pygame as py
py.init()
# Get display info
display_info = py.display.Info()
# Get actual screen width and height
screen_w = display_info.current_w
screen_h = display_info.current_h 


import tkinter as tk

def get_screen_width_in_inches():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.update_idletasks()
    width_mm = root.winfo_screenmmwidth()
    width_inches = width_mm / 25.4
    root.destroy()
    return width_inches

screen_width_inches = get_screen_width_in_inches()
