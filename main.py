from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

def input(address):
    text = open(address, "r")
    rows, cols = map(int, text.readline().split())
    table = [text.readline().split() for j in range(rows)]
    print(table)
    return table, cols


def map_IDS(table, cols):
    check = False
    for i in range(len(table)):
        for j in range (cols):
                if 'r' in table[i][j]:
                    xR , yR = i, j
                    check = True
                    break
        if check : break
    g = Graph(len(table)*cols)
    explored, frontier = [], []
    frontier.append(xR * cols +yR)
    while len(frontier) >0:
        # print('1', node)
        xDis, yDis = int(frontier[0]/cols), frontier[0]%cols
        # print(xDis, yDis)
        if 0 < xDis < len(table) and ((xDis - 1) * cols + yDis) not in explored:       #up
            # print(1,'          ', xDis-1, yDis)
            g.addEdge(xDis * cols + yDis, (xDis - 1) * cols + yDis)
            if ((xDis - 1) * cols + yDis) not in frontier:
                frontier.append((xDis - 1) * cols + yDis)
        if 0 <= xDis < len(table)-1 and ((xDis + 1) * cols + yDis) not in explored:  # down
            # print(2,'          ', xDis+1, yDis)
            g.addEdge(xDis * cols + yDis, (xDis + 1) * cols + yDis)
            if ((xDis + 1) * cols + yDis) not in frontier:
                frontier.append((xDis + 1) * cols + yDis)
        if 0 < yDis < cols and (xDis * cols + yDis - 1) not in explored:       #left
            # print(3,'          ', xDis, yDis-1)
            g.addEdge(xDis * cols + yDis, xDis * cols + yDis-1)
            if (xDis * cols + yDis - 1) not in frontier:
                frontier.append(xDis * cols + yDis - 1)
        if 0 <= yDis < cols-1 and (xDis * cols + yDis + 1) not in explored:        #right
            # print(4,'          ', xDis, yDis+1)
            g.addEdge(xDis * cols + yDis, xDis * cols + yDis+1)
            if (xDis * cols + yDis + 1) not in frontier:
                frontier.append(xDis * cols + yDis + 1)
        if (xDis * cols + yDis) not in explored:
            explored.append(xDis * cols + yDis)
        frontier.remove(xDis * cols + yDis)
        print('explored', explored)
        print('frontier', frontier)

    print(g.graph)








class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

'''
find the path from r to all the butters!! and print the path
'''
def A_star(start, end, table, cols):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    maze = table
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 'x':
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            if 'r' in maze[int(child.position[0])][int(child.position[1])] or 'b' in maze[int(child.position[0])][int(child.position[1])]:
                child.h = 0
            else:
                child.h = int(maze[int(child.position[0])][int(child.position[1])])
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    check = False
    table, cols = input("test1.txt")
    xB = []
    yB = []
    for i in range(len(table)):
        for j in range(cols):
            if 'r' in table[i][j]:
                xR, yR = i, j
                check = True
                break
        if check: break
    check = False

    for i in range(len(table)):
        for j in range(cols):
            if 'b' in table[i][j]:
                xB.append(i)
                yB.append(j)
                check = True
                break
        if check: break
    start = (1, 0)
    end = (0, 1)
    path_directions = []
    for i in range(len(xB)):
        start = (xR, yR)
        end = (xB[i], yB[i])
        path = A_star(start, end, table, cols)
        for j in range(len(path) - 1):
            if path[j][0] == path[j+1][0]:
                if path[j][1] > path[j+1][1]:
                    path_directions.append("L")
                else:
                    path_directions.append("R")
            elif path[j][1] == path[j][1]:
                if path[j][0] > path[j+1][0]:
                    path_directions.append("U")
                else:
                    path_directions.append("D")
        print(path)
        print(*path_directions, sep=" ")

if __name__ == '__main__':
    # table, cols = input("test1.txt")
    # map_IDS(table, cols)
    main()
