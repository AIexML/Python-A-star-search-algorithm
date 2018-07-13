from tkinter import *
import random
import time
from astar import *


#  CONSTANTS
TIME = 0.05
CELL_SIZE = 40
NUMBER_OF_OBSTACLES = 90
SIZE = 16

STATE_OBSTACLE = 0
STATE_START = 1
STATE_END = 2

#  GLOBALS
obstacles = []
current_state = None
start = None
end = None


def refresh_map():
    global CELL_SIZE, SIZE, start, end
    
    grid.delete(ALL)
    
    for x in range(SIZE):
        grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)
        
    for obstacle in obstacles:
        x, y = obstacle
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

    if start:
        x1, y1 = start
        grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')

    if end:
        x2, y2 = end
        grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')


def create_path():
    global CELL_SIZE, SIZE, current_state, start, end
    
    current_state = None
    start_button.config(state=DISABLED)
    custom_button.config(state=DISABLED)
    refresh_map()

    if not start and not end:
        get_random_positions()

    print("path between", start, end)
    x1, y1 = start
    x2, y2 = end

    grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    root.update()
    
    path, debug = get_path(start, end, obstacles, SIZE)
    
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
    start_button.config(state=NORMAL)
    custom_button.config(state=NORMAL)
    start = None
    end = None


def custom(state):
    global obstacles, current_state
    
    if state == STATE_OBSTACLE:
        start_button.config(state=DISABLED)
        current_state = STATE_OBSTACLE
        custom_button.config(text="set the start", command=lambda:custom(STATE_START))
        refresh_map()
        
    elif state == STATE_START:
        current_state = STATE_START
        custom_button.config(text="set the end", command=lambda:custom(STATE_END))
        
    elif state == STATE_END:
        current_state = STATE_END
        custom_button.config(text="set the obstacles", command=lambda:custom(STATE_OBSTACLE))
    

def click(event):
    global obstacles, current_state, start, end
    
    x, y = event.x//CELL_SIZE, event.y//CELL_SIZE
    
    if current_state == STATE_OBSTACLE:
        if (x, y) in obstacles:
            obstacles.remove((x, y))
        else:
            obstacles.append((x, y))
        refresh_map()
        
    elif current_state == STATE_START:
        if (x, y) not in obstacles:
            start = (x, y)
            refresh_map()

    elif current_state == STATE_END:
        if (x, y) not in obstacles and (x, y) != start:
            end = (x, y)
            refresh_map()
            start_button.config(state=NORMAL)


def get_random_positions():
    global start, end
    
    start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    while start in obstacles:
        start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    end = start
    while end == start or end in obstacles:
        end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))


root = Tk()

grid_frame = Frame(root)
grid_frame.grid(row=0, column=0)

button_frame = Frame(root)
button_frame.grid(row=1, column=0)

grid = Canvas(grid_frame, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='white')
grid.bind("<Button-1>", click)
grid.pack()

for x in range(SIZE):
    grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
    grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

for i in range(NUMBER_OF_OBSTACLES):
    x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
    obstacles.append((x, y))
    grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

frame_start_button = Frame(button_frame, width=SIZE*CELL_SIZE//2, height=100)
frame_start_button.propagate(False)
frame_start_button.grid(row=0, column=0)
start_button = Button(frame_start_button, text='start', command=create_path)
start_button.pack(expand=True, fill=BOTH)

frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE//2, height=100)
frame_custom_button.propagate(False)
frame_custom_button.grid(row=0, column=1)
custom_button = Button(frame_custom_button, text='set the obstacles', command=lambda:custom(STATE_OBSTACLE))
custom_button.pack(expand=True, fill=BOTH)

root.mainloop()
