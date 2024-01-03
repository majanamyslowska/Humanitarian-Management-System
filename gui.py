from tkinter import *

def submit():
    username = entry.get()
    print("Hello "+username)

def delete():
    entry.delete(0,END) # deletes the line of text

def backspace():
    entry.delete(len(entry.get())-1,END) # delete last character

def main_account_screen():
    main_screen = Tk()
    main_screen.geometry('300x250')
    main_screen.title("")

window = Tk()

submit = Button(window,text = "submit", command = submit)
submit.pack(side = RIGHT)

delete = Button(window,text = "delete", command = delete)
delete.pack(side = RIGHT)

backspace = Button(window,text = "backspace", command = backspace)
backspace.pack(side = RIGHT)

entry = Entry()
entry.config(font =('Hevetica', 13))
entry.pack()
entry.config(width=10)

window.mainloop()