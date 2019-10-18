from tkinter import *
from tkinter import messagebox


class Prompt:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.lbl = Label(frame, text='Please input n')
        self.lbl.grid(row=0)

        self.e = Entry(frame)
        self.e.grid(row=0, column=1)
        self.e.focus_set()

        self.btn = Button(frame, text='Generate Maze', command=self.generateMaze)
        self.btn.grid(columnspan=2, row=1)

    def generateMaze(self):
        input = self.e.get()
        if int(input) < 8 or int(input) > 64:
            messagebox.showerror('Invalid Input', message='Please enter a valid number')
        else:
            print('STUFF')

class Maze:
    colorBG = "red"
    emptyColor = "white"
    colorBorder = "red"
    emptyBorder = "black"

    def __init__(self, master, x, y):
        frame = Frame(master)


root = Tk()
start = Prompt(root)
root.mainloop()

