from tkinter import *
from tkinter import messagebox
import time
from collections import deque
from itertools import product, starmap, islice


class Prompt:
    def __init__(self, master):
        self.master = master
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
            self.master.destroy()
            app = Tk()

            if int(input) < 25:
                cellSize = 30
            else:
                cellSize = 15

            grid = CellGrid(app, int(input), int(input), cellSize)
            grid.pack()
            #btn.pack()


            app.mainloop()


#https://stackoverflow.com/questions/30023763/how-to-make-an-interactive-2d-grid-in-a-window-in-python
class Cell():
    FILLED_COLOR_BG = "black"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"
    START_STATE = "green"
    END_STATE = "red"
    VISITED_STATE = "yellow"
    PATH_STATE = "orange"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False
        self.visited = False
        self.start = False
        self.end  = False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """

        if self.master != None :
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                #fill = Cell.START_STATE
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
    def drawStart(self):
        fill = Cell.START_STATE
        outline = Cell.EMPTY_COLOR_BORDER

        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size

        self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)

    def drawEnd(self):
        fill = Cell.END_STATE
        outline = Cell.EMPTY_COLOR_BORDER

        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size

        self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)

    def drawPath(self):
        if not self.visited:
            self.visited = True

        fill = Cell.VISITED_STATE
        outline = Cell.FILLED_COLOR_BORDER

        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size

        self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)



class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.boardSize = rowNumber

        #initilize the queues & BFS for the BFS algorithm
        self.q1 = deque()
        self.path = []
        self.correctPath ={}
        self.walls = []
        self.visited = set()

        self.cellSize = cellSize
        self.button = Button(master, text="Solve Maze", command=self.drawPath)
        self.button.pack()

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def drawPath(self):
        # print("Please work")
        # print(self.grid[0][0].abs)
        # print(self.grid[1][1].abs)
        # print(self.grid[1][1].fill)
        self.findWalkAble()

        # print("({}, {}".format(self.grid[7][7].abs, self.grid[7][7].ord))
        #
        # print(self.findNeighbors(self.grid[0][0].abs, self.grid[0][0].ord))
        # print(self.findNeighbors(self.grid[7][7].abs, self.grid[7][7].ord))
        # print(self.findNeighbors(self.grid[0][5].abs, self.grid[0][5].ord))

        curX = 0
        curY = 0

        self.q1.append((curX, curY))
        self.correctPath[curX, curY] = curX, curY

        while len(self.q1) > 0:
            x, y = self.q1.popleft()

            if(x-1, y) in self.path and (x -1, y) not in self.visited:
                cell = (x-1, y)
                self.correctPath[cell] = x, y
                self.q1.append(cell)
                self.visited.add((x-1, y))

            if (x, y+1) in self.path and (x, y+1) not in self.visited:
                cell = (x, y+1)
                self.correctPath[cell] = x, y
                self.q1.append(cell)
                self.visited.add((x, y+1))
                #print(self.correctPath)

            if (x+1, y) in self.path and (x+1, y) not in self.visited:
                cell = (x+1, y)
                self.correctPath[cell] = x, y
                self.q1.append(cell)
                self.visited.add((x+1, y))

            if (x, y-1) in self.path and (x, y-1) not in self.visited:
                cell = (x, y-1)
                self.correctPath[cell] = x, y
                self.q1.append(cell)
                self.visited.add((x, y-1))

        print("curX is {} and curY is {}".format(curX, curY))
        self.backTrace()

    def backTrace(self):
        print("The path to take is this: ")
        curX = self.boardSize-1
        curY = curX

        while (curX, curY) != (0, 0):
            print(self.correctPath[curX, curY])
            curX, curY =self.correctPath[curX, curY]


    def findWalkAble(self):
        for row in self.grid:
            for cell in row:
                if cell.fill == False:
                    self.path.append((cell.abs, cell.ord))
                else:
                    self.walls.append((cell.abs, cell.ord))


    def draw(self):
        skip = False
        for row in self.grid:
            for cell in row:
                if skip == False:
                    cell.start = True
                    cell.drawStart()
                    skip = True
                else:
                    cell.draw()

        cell.drawEnd()
        cell.end = True

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        if(cell.start == True or cell.end == True):
            print("Do Nothing")
        else:
            cell._switch()
            cell.draw()
            #add the cell to the list of cell switched during the click
            self.switched.append(cell)



root = Tk()
start = Prompt(root)
root.mainloop()

