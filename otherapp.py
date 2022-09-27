from tkinter import *
from namer import nameit

root = Tk()
root.title("My Efforts to learn New")
root.geometry("600x400")

def submit():
    greet = nameit(my_box.get())
    my_label.config(text=greet)


my_box = Entry(root)
my_box.pack(pady=20)

my_label = Label(root, text="", font=("Helvetica", 18))
my_label.pack(pady=20)

my_button = Button(root, text="Submit Name", command=submit)
my_button.pack(pady=20)


root.mainloop()