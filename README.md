# Intelligent
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


def map_IDS(g, table, cols, typeStart, typeTarget):
    for i in range(len(table)):
        for j in range (cols):
                if ('r' in table[i][j] and typeStart == 'r') or ('b' in table[i][j] and typeStart == 'b'):
                    xHead , yHead = i, j
                if ('b' in table[i][j] and typeTarget == 'b') or ('p' in table[i][j] and typeTarget == 'p'):
                    xTarget , yTarget = i, j
    # g = Graph(len(table)*cols)
    explored, frontier = [], []
    frontier.append(xHead * cols +yHead)
    while len(frontier) >0:
        # print('1', node)
        # if target == frontier[0]:
        #     print('you found the goal')
        #     print(g.graph)
        xNode, yNode = int(frontier[0]/cols), frontier[0]%cols
        # print(xDis, yDis)
        if 0 < xNode < len(table) and ((xNode - 1) * cols + yNode) not in explored:       #up
            # print(1,'          ', xDis-1, yDis)
            if xNode-1 == xTarget and yNode==yTarget:
                g.addEdge(xNode * cols + yNode, (xNode - 1) * cols + yNode)
                # print('you found the goal')
                return g, (xNode - 1) * cols + yNode
            # else:
            elif 'x' not in table[xNode-1][yNode]:
                g.addEdge(xNode * cols + yNode, (xNode - 1) * cols + yNode)
                if ((xNode - 1) * cols + yNode) not in frontier:
                    frontier.append((xNode - 1) * cols + yNode)
        if 0 <= xNode < len(table)-1 and ((xNode + 1) * cols + yNode) not in explored:  # down
            # print(2,'          ', xDis+1, yDis)
            if xNode+1 == xTarget and yNode==yTarget:
                g.addEdge(xNode * cols + yNode, (xNode + 1) * cols + yNode)
                # print('you found the goal')
                return g, (xNode + 1) * cols + yNode
            # else:
            elif 'x' not in table[xNode + 1][yNode]:
                g.addEdge(xNode * cols + yNode, (xNode + 1) * cols + yNode)
                if ((xNode + 1) * cols + yNode) not in frontier:
                    frontier.append((xNode + 1) * cols + yNode)
        if 0 < yNode < cols and (xNode * cols + yNode - 1) not in explored:       #left
            # print(3,'          ', xDis, yDis-1)
            if xNode == xTarget and yNode-1==yTarget:
                g.addEdge(xNode * cols + yNode, xNode * cols + yNode-1)
                # print('you found the goal')
                return g, xNode* cols + yNode-1
            # else:
            elif 'x' not in table[xNode][yNode-1]:
                g.addEdge(xNode * cols + yNode, xNode * cols + yNode-1)
                if (xNode * cols + yNode - 1) not in frontier:
                    frontier.append(xNode * cols + yNode - 1)
        if 0 <= yNode < cols-1 and (xNode * cols + yNode + 1) not in explored:        #right
            # print(4,'          ', xDis, yDis+1)
            if xNode == xTarget and yNode+1==yTarget:
                g.addEdge(xNode * cols + yNode, xNode * cols + yNode + 1)
                # print('you found the goal')
                return g, xNode * cols + yNode+1
            # else:
            elif 'x' not in table[xNode][yNode+1]:
                g.addEdge(xNode * cols + yNode, xNode * cols + yNode+1)
                if (xNode * cols + yNode + 1) not in frontier:
                    frontier.append(xNode * cols + yNode + 1)
        if (xNode * cols + yNode) not in explored:
            explored.append(xNode * cols + yNode)
        frontier.remove(xNode * cols + yNode)
        # print('explored', explored)
        # print('frontier', frontier)
    # print(g.graph)
    return g, -1
    # print(g.graph)

def Path_IDS(g, target):

    key_list = list(g.graph.keys())
    val_list = list(g.graph.values())
    path = []
    # print(key_list)
    # print(val_list)
    # print(target)
    # goal = target
    path.append(target)
    for i in range (len(key_list)-1, -1, -1):
        # print(val_list[i])
        for j in range (len(val_list[i])):
            if target == val_list[i][j]:
                # path.append(target)
                path.append(key_list[i])
                target = key_list[i]
                # print(target)
    # path.append(goal)
    print('path', path)







if __name__ == '__main__':
    table, cols = input("test6.txt")
    g = Graph(len(table) * cols)
    g, target = map_IDS(g, table, cols, 'r', 'b')
    if target == -1:
        print('path in not reachable')
    else:
        print(g.graph, target)
        
