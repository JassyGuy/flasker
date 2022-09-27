from tkinter import *
from numpy import roots
import pygame

root = Tk()
root.title('Music Player')
root.geometry("500x300")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

control_frame = Frame(root)
control_frame.pack()

root.mainloop()