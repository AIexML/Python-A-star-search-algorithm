def get_distance(pos1, pos2):
    """Returns the Manhattan distance between pos1 and pos2"""
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def get_path(start, end, OBSTACLES, SIZE):
    """Returns a path between start and end if it exists and a list of cells analzyed"""
    if start == end:
        return None, []
    openList = [start]
    nodes = {start: ['',0]}  # nodes[(x, y)] = [parent, distance from the start]
    closedList = []
    x1, y1 = start
    while openList:
        current_node = openList[0]
        for tmp in openList[1:]:
            if nodes[tmp][1] + get_distance(tmp, end) < nodes[current_node][1] + get_distance(current_node, end):
                current_node = tmp
        x, y = current_node
        if current_node == end:
            break

        openList.remove(current_node)
        closedList.append(current_node)
        
        for a, b in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            X = current_node[0] + a
            Y = current_node[1] + b
            new_node = (X, Y)
            if new_node in OBSTACLES or new_node in closedList or X < 0 or X >= SIZE or Y < 0 or Y >= SIZE:
                continue
            elif not new_node in openList:
                openList.append(new_node)
                nodes[new_node] = [current_node, nodes[current_node][1] + 1]
            elif not new_node in nodes or nodes[new_node][1] > nodes[current_node][1] + 1:
                nodes[new_node] = [current_node, nodes[current_node][1] + 1]
        
    if current_node != end:  # if the path does not exist
        return None, closedList

    parent = nodes[end][0]
    path = [end]
    while parent != start:  # rewind the parents of the nodes to get the path
        path = [parent] + path
        parent = nodes[parent][0]
    return path, closedList
