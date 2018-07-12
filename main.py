from tkinter import *
import random
import time
from astar import *


TIME = 0.05
CELL_SIZE = 40
NUMBER_OF_OBSTACLES = 90
SIZE = 16


def refresh_map():
    global CELL_SIZE, SIZE
    grid.delete(ALL)
    for x in range(SIZE):
        grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)
    for obstacle in OBSTACLES:
        x, y = obstacle
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')


def create_path():
    global CELL_SIZE, SIZE
    startButton.config(state=DISABLED)
    refresh_map()
    pos1 = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    while pos1 in OBSTACLES:
        pos1 = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    pos2 = pos1
    while pos2 == pos1 or pos2 in OBSTACLES:
        pos2 = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))

    print("path between", pos1, pos2)
    x1, y1 = pos1
    x2, y2 = pos2

    grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    root.update()
    
    path, debug = get_path(pos1, pos2, OBSTACLES, SIZE)
    
    for cell in debug[1:]:
        x, y = cell
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='yellow')
        root.update()
        time.sleep(TIME)
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='#bbbbdd')
        
    if path:
        print("    length :", len(path))
        for cell in path[:-1]:
            x, y = cell
            grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='blue')
        percentage = round(len(path)*100/len(debug), 3)
    else:
        print("    length : no path")
        percentage = 0
    print("    {0} cells analyzed ({1}%)\n".format(len(debug), percentage))
    startButton.config(state=NORMAL)


root = Tk()
grid = Canvas(root, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='white')
grid.pack()
OBSTACLES = []
for x in range(SIZE):
    grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
    grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

for i in range(NUMBER_OF_OBSTACLES):
    x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
    OBSTACLES.append((x, y))
    grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

startButton = Button(root, text='start', command=create_path)
startButton.pack()
root.mainloop()
