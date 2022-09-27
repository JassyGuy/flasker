from tkinter import *
import PyPDF2
from tkinter import filedialog

root = Tk()
root. title('Benny Choe - Read PDF !')
root.geometry("500x500")

#Create a textbox
my_text = Text(root, height=30, width=60)
my_text.pack(pady=10)

#Create A Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Clear the textbox
def clear_text_box():
        my_text.delete(1.0, END)
        
#Open our pdf file
def open_pdf():
    open_file = filedialog.askopenfilename(
    initialdir="C:/mypjt",
    title="Open PDF file",
    filetypes=(
        ("PDF Files", "*.pdf"),
        ("All Files", "*.*"))
        )

    #Check to see if there is a file
    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        page = pdf_file.getPage(0)
        page_stuff = page.extractText()
        my_text.insert(1.0, page_stuff)
            
#Add some dropdown
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_pdf)
file_menu.add_command(label="Clear", command=clear_text_box)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)





    


root.mainloop()