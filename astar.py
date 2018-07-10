def getDistance(pos1, pos2):
    """Returns the Manhattan distance between pos1 and pos2"""
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def getPath(start, end, OBSTACLES):
    """Returns a path between start and end, if it exists"""
    if start == end:
        return -1
    openList = [start]
    nodes = {start : ['',0]} # nodes[(x, y)] = [parent, distance from the start]
    closedList = []
    x1, y1 = start
    while openList:
        current = openList[0]
        for tmp in openList:
            if nodes[tmp][1] + getDistance(tmp, end) < nodes[current][1] + getDistance(current, end):
                current = tmp
        x, y = current
        if current == end:
            break

        openList.remove(current)
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
        
    if current != end: # if the path does not exist
        return -1, closedList

    tmp = nodes[end][0]
    path = [end]
    while tmp != start: # rewind the parents of the nodes to get the path
        path.append(tmp)
        tmp = nodes[tmp][0]
    return path[::-1], closedList
