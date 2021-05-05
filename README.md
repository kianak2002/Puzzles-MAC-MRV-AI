# Intelligent
def input(address):
    text = open(address, "r")
    rows, cols = map(int, text.readline().split())
    table = [text.readline().split() for j in range(rows)]
    return table, cols

def start_destination(table, cols, typeStart, typeTarget):
    # xHead, yHead, xTarget, yTarget =0, 0, 0, 0
    for i in range(len(table)):
        for j in range(cols):
            if ('r' in table[i][j] and typeStart == 'r') or ('b' in table[i][j] and typeStart == 'b'):
                xHead, yHead = i, j
            if ('b' in table[i][j] and typeTarget == 'b') or ('p' in table[i][j] and typeTarget == 'p'):
                xTarget, yTarget = i, j
    return xHead, yHead, xTarget, yTarget

def IDS_R_To_B(table, cols, xHead, yHead, xTarget, yTarget):
    explored, frontier = [], []
    child = dict()
    frontier.append(xHead * cols + yHead)
    while len(frontier) > 0:
        xNode, yNode = int(frontier[0] / cols), frontier[0] % cols

        if 0 < xNode < len(table) and ((xNode - 1) * cols + yNode) not in explored:  # up
            if xNode - 1 == xTarget and yNode == yTarget:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode - 1][yNode]:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode - 1) * cols + yNode) not in frontier:
                    frontier.append((xNode - 1) * cols + yNode)

        if 0 <= xNode < len(table) - 1 and ((xNode + 1) * cols + yNode) not in explored:  # down
            if xNode + 1 == xTarget and yNode == yTarget:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode + 1][yNode]:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode + 1) * cols + yNode) not in frontier:
                    frontier.append((xNode + 1) * cols + yNode)

        if 0 < yNode < cols and (xNode * cols + yNode - 1) not in explored:  # left
            if xNode == xTarget and yNode - 1 == yTarget:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode][yNode - 1]:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                if (xNode * cols + yNode - 1) not in frontier:
                    frontier.append(xNode * cols + yNode - 1)

        if 0 <= yNode < cols - 1 and (xNode * cols + yNode + 1) not in explored:          # right
            if xNode == xTarget and yNode + 1 == yTarget:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode][yNode + 1]:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                if (xNode * cols + yNode + 1) not in frontier:
                    frontier.append(xNode * cols + yNode + 1)

        if (xNode * cols + yNode) not in explored:
            explored.append(xNode * cols + yNode)
        frontier.remove(xNode * cols + yNode)
    return -1



def IDS_B_To_P(table, cols, xNode, yNode, xTarget, yTarget):
    explored, frontier = [], []
    child = dict()
    frontier.append(xNode * cols + yNode)
    while len(frontier) > 0:
        xNode, yNode = int(frontier[0] / cols), frontier[0] % cols
        # print(table[xNode-1][yNode], xNode-1)
        if 0 < xNode < len(table)-1 and ((xNode - 1) * cols + yNode) not in explored and \
                table[xNode+1][yNode] != 'x' and IDS_R_To_B(table, cols, xNode-1, yNode, xNode+1, yNode) != -1:  # up
            if xNode - 1 == xTarget and yNode == yTarget:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif table[xNode - 1][yNode] != 'x':
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode - 1) * cols + yNode) not in frontier:
                    frontier.append((xNode - 1) * cols + yNode)

        if 0 < xNode < len(table) - 1 and ((xNode + 1) * cols + yNode) not in explored and \
                table[xNode-1][yNode] != 'x' and IDS_R_To_B(table, cols, xNode+1, yNode, xNode-1, yNode) != -1:  # down
            if xNode + 1 == xTarget and yNode == yTarget:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode + 1][yNode]:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode + 1) * cols + yNode) not in frontier:
                    frontier.append((xNode + 1) * cols + yNode)

        if 0 < yNode < cols-1 and (xNode * cols + yNode - 1) not in explored and \
                table[xNode][yNode+1] != 'x' and IDS_R_To_B(table, cols, xNode, yNode-1, xNode, yNode+1) != -1:  # left
            if xNode == xTarget and yNode - 1 == yTarget:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode][yNode - 1]:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                if (xNode * cols + yNode - 1) not in frontier:
                    frontier.append(xNode * cols + yNode - 1)

        if 0 < yNode < cols - 1 and (xNode * cols + yNode + 1) not in explored \
                and table[xNode][yNode-1] != 'x' and IDS_R_To_B(table, cols, xNode, yNode+1, xNode, yNode-1) != -1:   # right
            if xNode == xTarget and yNode + 1 == yTarget:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode][yNode + 1]:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                if (xNode * cols + yNode + 1) not in frontier:
                    frontier.append(xNode * cols + yNode + 1)

        if (xNode * cols + yNode) not in explored:
            explored.append(xNode * cols + yNode)
        frontier.remove(xNode * cols + yNode)
    return -1

def Path_IDS(childs, start, target, path):
    path.append(target)
    while True:
        path.append(childs.get(target))
        if start != childs.get(target):
            target = childs.get(target)
        else:
            return path

def R_to_B(path, cols):
    path.reverse()
    print(path)
    # for i in range (len(path)-2, -1, -1):
    for i in range (1, len(path)-1):
        if path[i+1] == path[i]+cols:
            print('D', end=' ')
        if path[i+1] == path[i]-cols:
            print('U', end=' ')
        if path[i+1] == path[i]+ 1:
            print('R', end=' ')
        if path[i+1] == path[i]-1:
            print('L', end=' ')



if __name__ == '__main__':
    table, cols = input("test7.txt")
    xHead, yHead, xTarget, yTarget = start_destination(table, cols, 'b', 'p')
    print(xHead, yHead, xTarget, yTarget)
    child = IDS_B_To_P(table, cols, xHead, yHead, xTarget, yTarget)
    print(child)
    # start, target, child = map_IDS(table, cols, xHead, yHead, xTarget, yTarget, 'b')
    if child == -1:
        print('path in not reachable')
        exit(0)
    else:
        path = []
        path = Path_IDS(child, xHead*cols + yHead, xTarget*cols + yTarget, path)
        print(path)
