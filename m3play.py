import os
from tkinter import *
from tkinter.filedialog import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk 

root = Tk()
root.title("MP3 플레이어")
root.geometry("500x400")

#Initialize Pygame Mixer
pygame.mixer.init()

def play_time():
    #Check for double timing ??
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos()/1000
    
    #slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
    
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'C:/music/{song}.mp3'    
    # Load Song with Mutagen
    song_mut = MP3(song)
    
    #Get Song Length
    global song_length
    song_length = song_mut.info.length
    #Convert ot time format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
    
    #status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
    # Update slider position to current song position....
    #my_slider.config(value=int(current_time))
    
     #Update Slider to position
    #slider_poisition = int(song_length)

    #Increase current time by 1 second
    current_time +=1
    
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}')
    elif paused:
        pass    
    elif int(my_slider.get()) == int(current_time):
        #Update Slider to position
        slider_poisition = int(song_length)
        my_slider.config(to=slider_poisition, value=int(current_time))
        
    else:
        #Update Slider to position
        slider_poisition = int(song_length)
        my_slider.config(to=slider_poisition, value=int(my_slider.get()))
        
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(my_slider.get()))
        #Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        
    # convert to time format
    # converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
        
        #Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    
    status_bar.after(1000, play_time)
    
#Create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/music/{song}.mp3'
     
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
     
# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=current_volume*100)
   
#Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

#Create Playlist Box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)


ls_music = []
index = 0
lb_string = StringVar()

def add_song():
    song = filedialog.askopenfilename(initialdir='C:/music/', title="Choose A Song", filetypes=(("mp3 files", "*.mp3"), ))
    #Strip out the directory info and .mp extension
    song = song.replace("C:/music/", "")
    song = song.replace(".mp3", "")

    song_box.insert(END, song)
    
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/music/', title="Choose A Song", filetypes=(("mp3 files", "*.mp3"), ))
    
    for song in songs:
        song = song.replace("C:/music/", "")
        song = song.replace(".mp3", "")

        song_box.insert(END, song)        
    
 
def play():

    #Set Stopped Variable To False So Song Can play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/music/{song}.mp3'
     
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
     
    play_time()
     
     #Update Slider to position
     #slider_poisition = int(song_length)
     #my_slider.config(to=slider_poisition, value=0)
 
global stopped
stopped = False
   
def stop():
    #Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #Stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    #Clear the status bar    
    status_bar.config(text='')
    
    #Set Stop Variable to True
    global stopped
    stopped = True


global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True    

def next_song():
    #Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/music/{song}.mp3'
     
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)      
    
    song_box.selection_clear(0, END)
    song_box.activate(next_one)      
    song_box.selection_set(next_one, last=None)
    

def previous_song():
    #Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = f'C:/music/{song}.mp3'
     
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)      
    
    song_box.selection_clear(0, END)
    song_box.activate(next_one)      
    song_box.selection_set(next_one, last=None)

def delete_song():
    stop()
    #Delete Currently Selected Song
    song_box.delete(ANCHOR)
    #Stop Music if it's playing
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()


def music_list():
    global index
    dir = askdirectory()
    os.chdir(dir)

    for files in os.listdir(dir):
        ls_music.append(files)

    pygame.mixer.music.load(ls_music[index])

    def list_select(event):
        lb_string.set("")
        index = int(lb.curselection()[0])
        pygame.mixer.music.load(ls_music[index])
        pygame.mixer.music.play()
        lb_string.set(ls_music[index])

    def list_insert():
        i = 0

        for song in ls_music:
            lb.insert(i, song)
            i += 1
        

    win = Toplevel(root)
    win.title("목록")
    sb = Scrollbar(win)
    sb.pack(side = RIGHT, fill = Y)
    lb = Listbox(win, width = 50, yscrollcommand = sb.set)
    lb.pack(side = LEFT)
    sb.config(command = lb.yview)
    song_lb = Label(textvariable=lb_string)
    song_lb.pack()
    list_insert()


    lb.bind("<<ListboxSelect>>", list_select)
            
   
    
#Create Player Control Buttons
#back_btn = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_w.gif")


play_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_p.gif")
#b_p = Button(root,height = 30, width = 30, image=img_p)
#b_p.place(x = 155, y =166)

pause_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_s.gif")
#b_s = Button(root, height = 30, width = 30, image=img_s)
#b_s.place(x = 195, y = 166)

back_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_b.gif")
#b_b = Button(root, height = 30, width = 40, image=img_b)
#b_b.place(x = 50, y = 166)

forward_btn_img =  PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_n.gif")
#b_n = Button(root, height = 30, width = 40, image=img_n)
#b_n.place(x = 290, y = 166)


stop_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_l.gif")
#b_l = Button(root, height = 47, width = 30, image=img_l, command=music_list)
#b_l.place(x = 326, y = 24)

volumeup_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_u.gif")
#b_u = Button(root, height = 30, width = 30, image=img_u)
#b_u.place(x = 176, y = 48)

volumedown_btn_img = PhotoImage(file = "C:/Mypjt/python coding/mypjt/md_d.gif")
#b_d = Button(root, height = 30, width = 30, image=img_d)
#b_d.place(x = 176, y = 288)

#Create Player Control Frames
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=1)
forward_button.grid(row=0, column=6)
play_button.grid(row=0, column=3)
pause_button.grid(row=0, column=4)
stop_button.grid(row=0, column=5)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)

#Add Many Songs to the Playlist
add_song_menu.add_command(label="Add Many Songs to Playlist", command=add_many_songs)

#Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

#Creare Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

#Create Temporary Slider Label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

root.mainloop()
