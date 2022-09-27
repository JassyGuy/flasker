import threading
 
def sum(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print("Subthread", total)
 
t = threading.Thread(target=sum, args=(1, 100000))
t.start()
 
print("Main Thread")

import  requests, time
 
def getHtml(url):
    resp = requests.get(url)
    time.sleep(1)
    print(url, len(resp.text), ' chars')
 
t2 = threading.Thread(target=getHtml, args=('http://google.com',))
t2.start()
 
print("### End ###")

from tkinter import *
import time
from random import randint

root = Tk()

def five_seconds():
    time.sleep(5)
    my_label.config(text="5 Seconds Is Up!")
    
def rando():
    random_label.config(text=f'Random Number: {randint(1, 100)}')

root.title("Exercise of threading")
root.geometry("500x400")

my_label = Label(root, text="Hello There!")
my_label.pack(pady=20)

my_button1 = Button(root, text="5 seconds", command=threading.Thread(target=five_seconds).start())
my_button1.pack(pady=20)

my_button2 = Button(root, text="Pick Random Number !!", command=rando)
my_button2.pack(pady=20)

random_label = Label(root, text="")
random_label.pack(pady=20)

root.mainloop()