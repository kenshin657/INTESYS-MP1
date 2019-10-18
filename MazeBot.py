from tkinter import *


class Prompt:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.lbl = Label(frame, text='Please input n')
        self.lbl.grid(row=0)

        self.e = Entry(frame)
        self.e.grid(row=0, column=1)
        self.e.focus_set()

        self.btn = Button(frame, text='Generate Maze', command=self.helloPrint)
        self.btn.grid(columnspan=2, row=1)

    def helloPrint(self):
        input = self.e.get()
        print('You input ' + input)


root = Tk()
start = Prompt(root)

root.mainloop()
