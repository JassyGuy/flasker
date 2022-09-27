import tkinter
import time

class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.timer = None
        self.master = master
        self.master.title("simple timer")
        self.pack(fill='both', expand=True)

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.label = tkinter.Label(self, text=str(now))
        self.label.pack(padx=10, pady=10)

        self.start_button = tkinter.Button(self, text='start')
        self.start_button.pack(side='left', padx=10, pady=10)
        self.start_button.bind("<Button-1>", self.startTimer)
        self.stop_button = tkinter.Button(self, text='stop', state='disabled')
        self.stop_button.pack(side='left', padx=10, pady=10)
        self.stop_button.bind("<Button-1>", self.stopTimer)

    def startTimer(self, *_):
        self.tiktok()
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
    
    def stopTimer(self, *_):
        self.after_cancel(self.timer)
        self.stop_button.configure(state='disabled')
        self.start_button.configure(state='normal')

    def tiktok(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.label.config(text=str(now))
        self.timer = self.after(1000, self.tiktok)

root = tkinter.Tk()
root.geometry("300x100+100+100")
app = Application(root)
app.mainloop()