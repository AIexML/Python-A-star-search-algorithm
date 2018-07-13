from tkinter import *
import random
import time
from astar import *


TIME = 0.05
CELL_SIZE = 40
NUMBER_OF_OBSTACLES = 90
SIZE = 16


STATE_OBSTACLE = 0
STATE_START = 1
STATE_END = 2

def refresh_map():
    global CELL_SIZE, SIZE, start, end
    grid.delete(ALL)
    for x in range(SIZE):
        grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)
    for obstacle in OBSTACLES:
        x, y = obstacle
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

    if start:
        x1, y1 = start
        grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')

    if end:
        x2, y2 = end
        grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')


def create_path():
    global CELL_SIZE, SIZE, start, end
    startButton.config(state=DISABLED)
    customButton.config(state=DISABLED)
    refresh_map()

    if not start and not end:
        get_random_positions()

    print("path between", start, end)
    x1, y1 = start
    x2, y2 = end

    grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    root.update()
    
    path, debug = get_path(start, end, OBSTACLES, SIZE)
    
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
    customButton.config(state=NORMAL)
    start = None
    end = None


def custom(state):
    global OBSTACLES, current_state
    
    if state == STATE_OBSTACLE:
        startButton.config(state=DISABLED)
        current_state = STATE_OBSTACLE
        customButton.config(text="place start", command=lambda:custom(STATE_START))
        refresh_map()
        print("place obstacles")
        
    elif state == STATE_START:
        current_state = STATE_START
        customButton.config(text="place end", command=lambda:custom(STATE_END))
        
    elif state == STATE_END:
        current_state = STATE_END
        customButton.config(text="place obstacles", command=lambda:custom(STATE_OBSTACLE))
    

def click(event):
    global OBSTACLES, current_state, start, end
    x, y = event.x//CELL_SIZE, event.y//CELL_SIZE
    if current_state == STATE_OBSTACLE:
        if (x, y) in OBSTACLES:
            OBSTACLES.remove((x, y))
        else:
            OBSTACLES.append((x, y))
        refresh_map()
        
    elif current_state == STATE_START:
        if (x, y) not in OBSTACLES:
            start = (x, y)
            refresh_map()

    elif current_state == STATE_END:
        if (x, y) not in OBSTACLES and (x, y) != start:
            end = (x, y)
            refresh_map()
            startButton.config(state=NORMAL)


def get_random_positions():
    global start, end
    start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    while start in OBSTACLES:
        start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    end = start
    while end == start or end in OBSTACLES:
        end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    

current_state = None
start = None
end = None

root = Tk()
grid = Canvas(root, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='white')
grid.bind("<Button-1>", click)
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

customButton = Button(root, text='place obstacles', command=lambda:custom(STATE_OBSTACLE))
customButton.pack()

root.mainloop()
