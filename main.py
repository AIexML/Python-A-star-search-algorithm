from tkinter import *
import random
import time
from astar import *

TIME = 0.05
CELL_SIZE = 40
NUMBER_OF_OBSTACLES = 90

def refreshMap():
    global CELL_SIZE
    grid.delete(ALL)
    for x in range(16):
        grid.create_line(0, x*CELL_SIZE, 16*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, 16*CELL_SIZE)
    for obstacle in OBSTACLES:
        x, y = obstacle
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

def create_path():
    startButton.config(state=DISABLED)
    global CELL_SIZE
    refreshMap()
    pos1 = (random.randint(0,15), random.randint(0,15))
    while pos1 in OBSTACLES:
        pos1 = (random.randint(0,15), random.randint(0,15))
    pos2 = pos1
    while pos2 == pos1 or pos2 in OBSTACLES:
        pos2 = (random.randint(0,15), random.randint(0,15))

    print("path between", pos1, pos2, "length : ", end="")
    x1, y1 = pos1
    x2, y2 = pos2

    grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    root.update()
    path, debug = getPath(pos1, pos2, OBSTACLES)
    for cell in debug[1:]:
        x, y = cell
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='yellow')
        root.update()
        time.sleep(TIME)
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='#bbbbdd')
    if path != -1:
        print(len(path))
        for cell in path[:-1]:
            x, y = cell
            grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='blue')
    else:
        print("NO PATH")
    print("(" + str(len(debug)) + " cells analyzed)")
    startButton.config(state=NORMAL)

root = Tk()
grid = Canvas(root, width=16*CELL_SIZE, height=16*CELL_SIZE, bg='white')
grid.pack()
OBSTACLES = []
for x in range(16):
    grid.create_line(0, x*CELL_SIZE, 16*CELL_SIZE, x*CELL_SIZE)
    grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, 16*CELL_SIZE)

for i in range(NUMBER_OF_OBSTACLES):
    x, y = random.randint(0, 15), random.randint(0, 15)
    OBSTACLES.append((x, y))
    grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

startButton = Button(root, text='start', command=create_path)
startButton.pack()
root.mainloop()
