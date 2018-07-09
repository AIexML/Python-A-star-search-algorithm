from tkinter import *
import random
import time

root = Tk()

TIME = 0.05

CELL_SIZE = 40

NUMBER_OF_OBSTACLES = 90

def getDistance(pos1, pos2):
    """Returns the Manhattan distance between pos1 and pos2"""
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def getPath(start, end):
    """Returns a path between start and end, if it exists"""
    global OBSTACLES
    if start == end:
        return -1
    openList = [start]
    nodes = {start : ['',0]} # nodes['[x, y]'] = [parent, distance from the start]
    closedList = []
    x1, y1 = start
    while openList:
        current = openList[0]
        for tmp in openList:
            if nodes[tmp][1] + getDistance(tmp, end) < nodes[current][1] + getDistance(current, end):
                current = tmp
        x, y = current
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='yellow')
        grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
        if current == end:
            break

        del openList[openList.index(current)]
        closedList.append(current)
        
        for a,b in [(0,1), (0,-1), (1,0), (-1,0)]:
            X = current[0] + a
            Y = current[1] + b
            if (X, Y) in OBSTACLES or (X,Y) in closedList or X < 0 or X > 15 or Y < 0 or Y > 15:
                continue
            elif not (X,Y) in openList:
                openList.append((X,Y))
                nodes[(X,Y)] = [current, nodes[current][1] + 1]
            elif not (X,Y) in nodes or nodes[(X,Y)][1] > nodes[current][1] + 1:
                nodes[(X,Y)] = [current, nodes[current][1] + 1]
        root.update()
        
        time.sleep(TIME)
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='#bbbbdd')

    if current != end: # if the path does not exist
        return -1

    tmp = nodes[end][0]
    path = [end]
    while tmp != start: # rewind the parents of the nodes to get the path
        path.append(tmp)
        tmp = nodes[tmp][0]
    return path[::-1]

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
    startButton.config(state = DISABLED)
    global CELL_SIZE
    refreshMap()
    pos1 = (random.randint(0,15), random.randint(0,15))
    while pos1 in OBSTACLES:
        pos1 = (random.randint(0,15), random.randint(0,15))
    pos2 = pos1
    while pos2 == pos1 or pos2 in OBSTACLES:
        pos2 = (random.randint(0,15), random.randint(0,15))

    print("path between ", pos1, pos2)
    x1, y1 = pos1
    x2, y2 = pos2

    grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    root.update()
    time.sleep(TIME)
    path = getPath(pos1, pos2)
    if path != -1:
        for cell in path:
            x, y = cell
            grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='blue')
    else:
        print("NO PATH")
    grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')
    
    startButton.config(state = NORMAL)

grid = Canvas(root, width = 16*CELL_SIZE, height = 16*CELL_SIZE, bg = 'white')
grid.pack()
OBSTACLES = []
for x in range(16):
    grid.create_line(0, x*CELL_SIZE, 16*CELL_SIZE, x*CELL_SIZE)
    grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, 16*CELL_SIZE)

for i in range(NUMBER_OF_OBSTACLES):
    x, y = random.randint(0, 15), random.randint(0, 15)
    OBSTACLES.append((x, y))
    grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')
    
startButton = Button(root, text = 'start', command = create_path)
startButton.pack()

root.mainloop()
