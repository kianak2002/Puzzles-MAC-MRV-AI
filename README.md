def input(address):
    text = open(address, "r")
    rows, cols = map(int, text.readline().split())
    table = [text.readline().split() for j in range(rows)]
    return table, cols

def start_destination(table, cols, typeStart, typeTarget):
    # xHead, yHead, xTarget, yTarget = [], [], [], []
    Head, Target, Robot = [], [], []
    for i in range(len(table)):
        for j in range(cols):
            if 'r' in table[i][j]:
                Robot.append([i, j])
            # elif 'b' in table[i][j]:
            if ('r' in table[i][j] and typeStart == 'r') or ('b' in table[i][j] and typeStart == 'b'):
                # xHead, yHead = i, j
                # xHead.append(i)
                # yHead.append(j)
                Head.append([i, j])
            if ('b' in table[i][j] and typeTarget == 'b') or ('p' in table[i][j] and typeTarget == 'p'):
                # xTarget, yTarget = i, j
                # xTarget.append(i)
                # yTarget.append(j)
                Target.append([i, j])
    # return xHead, yHead, xTarget, yTarget
    return Head, Target, Robot
def IDS_R_To_B(table, cols, xHead, yHead, xTarget, yTarget, avoid):
    explored, frontier = [], []
    child = dict()
    frontier.append(xHead * cols + yHead)
    while len(frontier) > 0:
        xNode, yNode = int(frontier[0] / cols), frontier[0] % cols

        if 0 < xNode < len(table) and ((xNode - 1) * cols + yNode) not in explored and ((xNode - 1) * cols + yNode) != avoid:  # up
            if xNode - 1 == xTarget and yNode == yTarget:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode - 1][yNode]:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode - 1) * cols + yNode) not in frontier:
                    frontier.append((xNode - 1) * cols + yNode)

        if 0 <= xNode < len(table) - 1 and ((xNode + 1) * cols + yNode) not in explored  and ((xNode + 1) * cols + yNode) != avoid:  # down
            if xNode + 1 == xTarget and yNode == yTarget:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode + 1][yNode]:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode + 1) * cols + yNode) not in frontier:
                    frontier.append((xNode + 1) * cols + yNode)

        if 0 < yNode < cols and (xNode * cols + yNode - 1) not in explored and (xNode * cols + yNode - 1) != avoid:  # left
            if xNode == xTarget and yNode - 1 == yTarget:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                return child
            elif 'x' not in table[xNode][yNode - 1]:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                if (xNode * cols + yNode - 1) not in frontier:
                    frontier.append(xNode * cols + yNode - 1)

        if 0 <= yNode < cols - 1 and (xNode * cols + yNode + 1) not in explored and (xNode * cols + yNode + 1) != avoid: # right
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
    # print( xNode, yNode, xTarget, yTarget)
    while len(frontier) > 0:
        # print(child)
        # print(explored, frontier, len(frontier))
        xNode, yNode = int(frontier[0] / cols), frontier[0] % cols
        # print(explored)
        # print(yNode, cols - 1, explored, table[xNode][yNode-1], IDS_R_To_B(table, cols, xNode, yNode+1, xNode, yNode-1, xNode*cols+yNode+1))
        if 0 < xNode < len(table)-1 and ((xNode - 1) * cols + yNode) not in explored and table[xNode+1][yNode] != 'x' and \
                IDS_R_To_B(table, cols, xNode-1, yNode, xNode+1, yNode, (xNode-1)*cols+yNode) != -1:  # up
            if xNode - 1 == xTarget and yNode == yTarget:
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                # print(1)
                return child
            elif table[xNode - 1][yNode] != 'x':
                child[(xNode - 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode - 1) * cols + yNode) not in frontier:
                    frontier.append((xNode - 1) * cols + yNode)

        if 0 < xNode < len(table) - 1 and ((xNode + 1) * cols + yNode) not in explored and table[xNode-1][yNode] != 'x' \
                and IDS_R_To_B(table, cols, xNode+1, yNode, xNode-1, yNode, (xNode+1)*cols+yNode) != -1:  # down
            if xNode + 1 == xTarget and yNode == yTarget:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                # print(child)
                # print(2)
                return child
            elif 'x' not in table[xNode + 1][yNode]:
                child[(xNode + 1) * cols + yNode] = xNode * cols + yNode
                if ((xNode + 1) * cols + yNode) not in frontier:
                    frontier.append((xNode + 1) * cols + yNode)

        if 0 < yNode < cols - 1 and (xNode * cols + yNode + 1) not in explored and table[xNode][yNode-1] != 'x' and \
                IDS_R_To_B(table, cols, xNode, yNode+1, xNode, yNode-1, xNode*cols+yNode+1) != -1:   # right
            if xNode == xTarget and yNode + 1 == yTarget:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                # print(3)
                return child
            elif 'x' not in table[xNode][yNode + 1]:
                child[xNode * cols + yNode + 1] = xNode * cols + yNode
                if (xNode * cols + yNode + 1) not in frontier:
                    frontier.append(xNode * cols + yNode + 1)

        if 0 < yNode < cols-1 and (xNode * cols + yNode - 1) not in explored and table[xNode][yNode+1] != 'x' and \
                IDS_R_To_B(table, cols, xNode, yNode-1, xNode, yNode+1, xNode*cols+yNode-1) != -1:  # left
            if xNode == xTarget and yNode - 1 == yTarget:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                # print(4)
                return child
            elif 'x' not in table[xNode][yNode - 1]:
                child[xNode * cols + yNode - 1] = xNode * cols + yNode
                if (xNode * cols + yNode - 1) not in frontier:
                    frontier.append(xNode * cols + yNode - 1)
        if (xNode * cols + yNode) not in explored:
            explored.append(xNode * cols + yNode)
        frontier.remove(xNode * cols + yNode)
        # print(child)
    # print('ldfkjvjske', explored, frontier)
    return -1

def Path_IDS(childs, start, target, path):
    # print( start, target, path)
    # print(childs)
    path.append(target)
    while True:
        path.append(childs.get(target))
        if start != childs.get(target):
            target = childs.get(target)
        else:
            return path

def R_to_B(path, cols, way):
    path.reverse()
    # print('R to B', path)
    for i in range (len(path)-1):
        if path[i+1] == path[i]+cols:
            # print('D', end=' ')
            way.append('D')
        if path[i+1] == path[i]-cols:
            # print('U', end=' ')
            way.append('U')
        if path[i+1] == path[i]+ 1:
            # print('R', end=' ')
            way.append('R')
        if path[i+1] == path[i]-1:
            # print('L', end=' ')
            # print(path[i], path[i+1])
            # print('rrrrrrrr')
            way.append('L')
            # way.join('L')
    # print(way)
    return way


def B_to_P(table, pathB, cols):
    pathB.reverse()
    # print('B to P', pathB)
    way = []
    way = R_to_B([pathB[1], pathB[0]], cols, way)
    # print('wa', way)
    # print('way111', way, pathB)
    for i in range(len(pathB) - 2):
        # print('way', way)
        # print( int(pathB[i+1]/cols), pathB[i+1]%cols, int(pathB[i+2]/cols), pathB[i+2]%cols)
        pathR, child = [], []
        if int(pathB[i+2]/cols) == int(pathB[i+1]/cols):
            if pathB[i+2]%cols == pathB[i+1]%cols+1:        #right
                # print(1)
                xTarget, yTarget = int(pathB[i+1]/cols), pathB[i+1]%cols-1
                # print(xTarget, yTarget)
                child = IDS_R_To_B(table, cols, int(pathB[i]/cols), pathB[i]%cols, xTarget, yTarget, pathB[i+1])
                if child != -1:
                    pathR = Path_IDS(child,pathB[i], xTarget*cols +yTarget, pathR)
                    way = R_to_B(pathR, cols, way)
                way.append('R')
            elif pathB[i+2]%cols == pathB[i+1]%cols-1:        #left
                # print(2)
                # print('way1', way)
                # print('hiiiiiiiiiii')
                xTarget, yTarget = int(pathB[i+1]/cols), pathB[i+1]%cols+1
                # print(int(pathB[i] / cols), pathB[i] % cols)
                # print(xTarget, yTarget)
                # print('way2', way)
                child = IDS_R_To_B(table, cols, int(pathB[i]/cols), pathB[i]%cols, xTarget, yTarget, pathB[i+1])
                if child != -1:
                    pathR = Path_IDS(child,pathB[i], xTarget*cols +yTarget, pathR)
                    way = R_to_B(pathR, cols, way)
                # print('hhhhhh')
                way.append('L')
        elif pathB[i + 2] % cols == pathB[i + 1] % cols:
            if int(pathB[i + 2]/ cols) == int(pathB[i + 1] / cols) + 1:  # down
                # print('-2', way)
                # print(3)
                # print('dooooooown')
                xTarget, yTarget = int(pathB[i + 1] / cols)-1, pathB[i + 1] % cols
                # print(int(pathB[i] / cols), pathB[i] % cols)
                # print(xTarget, yTarget)
                # print(int(pathB[i] / cols), pathB[i] % cols, xTarget, yTarget,pathB[i + 1])
                # print('-1', way)
                child = IDS_R_To_B(table, cols, int(pathB[i] / cols), pathB[i] % cols, xTarget, yTarget,pathB[i + 1])
                # print(child)
                if child != -1:
                    # print('0', way)
                    pathR = Path_IDS(child, pathB[i], xTarget * cols + yTarget, pathR)
                    # print(pathR)
                    # print('1', way)
                    way = R_to_B(pathR, cols, way)
                    # print('2', way)
                way.append('D')
            elif int(pathB[i + 2] / cols) == int(pathB[i + 1] / cols) - 1:  # up
                # print(4)
                xTarget, yTarget = int(pathB[i + 1] / cols)+1, pathB[i + 1] % cols
                child = IDS_R_To_B(table, cols, int(pathB[i] / cols), pathB[i] % cols, xTarget, yTarget,pathB[i + 1])
                if child != -1:
                    pathR = Path_IDS(child, pathB[i], xTarget * cols + yTarget, pathR)
                    way = R_to_B(pathR, cols, way)
                way.append('U')
    # print('path B to P', way)
    return way

if __name__ == '__main__':
    table, cols = input("test9.txt")
    Head, Target, Robot = start_destination(table, cols, 'b', 'p')
    ways = []
    points = []
    B_To_P = []
    for i in range (len(Head)):
        for j in range (len(Target)):
            # print(Head[i], Target[j])
            child = IDS_B_To_P(table, cols, Head[i][0], Head[i][1], Target[j][0], Target[j][1])
            if child == -1:
                continue
            else:
                pathB_To_P = Path_IDS(child, Head[i][0] * cols + Head[i][1], Target[j][0] * cols + Target[j][1], [])
                xHead, yHead = Head[i][0], Head[i][1]
                if xHead == int(pathB_To_P[len(pathB_To_P) - 2] / cols):
                    if yHead == pathB_To_P[len(pathB_To_P)-2] % cols - 1:
                        yHead -= 1
                    elif yHead == pathB_To_P[len(pathB_To_P)-2] % cols + 1:
                        yHead += 1
                elif yHead == pathB_To_P[len(pathB_To_P)-2] % cols:
                    if xHead == int(pathB_To_P[len(pathB_To_P)-2] / cols) - 1:
                        xHead -= 1
                    if xHead == int(pathB_To_P[len(pathB_To_P)-2] / cols) + 1:
                        xHead += 1
                # print(xHead, yHead, Target[j])
                child2 = IDS_R_To_B(table, cols, Robot[0][0], Robot[0][1], xHead, yHead, pathB_To_P[len(pathB_To_P) - 1])
                way, wayR_To_B = [], []
                if Robot[0][0] == xHead and Robot[0][1] == yHead:
                    pathR_To_B = []
                elif child2 == -1:
                    continue
                else:
                    pathR_To_B = Path_IDS(child2, Robot[0][0] * cols + Robot[0][1], xHead* cols + yHead, [])
                wayR_To_B = R_to_B(pathR_To_B, cols, [])
                wayB_To_P = B_to_P(table, pathB_To_P, cols)
                B_To_P.append(wayB_To_P)
                for k in range (len(wayB_To_P)):
                    wayR_To_B.append(wayB_To_P[k])
                # print('R TO B', wayR_To_B)
                points.append([Head[i], Target[j], [xHead, yHead]])
                ways.append(wayR_To_B)
                # print('\n\n\n\n')
    # print(B_To_P)
    # print(points)
    # print(ways)

    if len(ways)==1:
        for i in range (len(ways[0])):
            print(ways[0][i], end=' ')
        exit(0)
    # print()
    # print()

    pointsT, waysT, B_To_PT = [], [], []
    for i in range (len(Head)):
        min = float('inf')
        index = -1
        for j in range (len(points)):
            if Head[i] == points[j][0] and min > len(ways[j]):
                min = len(ways[j])
                index = j
        if len(points)== 0:
            print('The path is not reachable')
            exit(0)
        B_To_PT.append(B_To_P[index])
        pointsT.append(points[index])
        waysT.append(ways[index])
    # print(B_To_PT)
    # print(pointsT)
    # print(waysT)


    for i in range (len(waysT)):    #points[b, p, starrtR, finishR]
        if waysT[i][len(waysT[i]) - 1] == 'U':
            pointsT[i].append([pointsT[i][1][0]+1, pointsT[i][1][1]])
        if waysT[i][len(waysT[i])-1] == 'D':
            pointsT[i].append([pointsT[i][1][0]-1, pointsT[i][1][1]])
        if waysT[i][len(waysT[i])-1] == 'R':
            pointsT[i].append([pointsT[i][1][0], pointsT[i][1][1]-1])
        if waysT[i][len(waysT[i])-1] == 'U':
            pointsT[i].append([pointsT[i][1][0]+1, pointsT[i][1][1]+1])
    # print(pointsT)

    for i in range (len(waysT)-1):
        for j in range (len(waysT[i])):
            print(waysT[i][j], end=' ')
        print()
        if i< len(waysT):
            child1 = IDS_R_To_B(table, cols, pointsT[i][3][0], pointsT[i][3][1], pointsT[i+1][2][0], pointsT[i+1][2][1], pointsT[i+1][0][0]*cols + pointsT[i+1][0][1])
            path1 = Path_IDS(child1, pointsT[i][3][0]*cols+ pointsT[i][3][1], pointsT[i+1][2][0]*cols+ pointsT[i+1][2][1], [])
            way1 = R_to_B(path1, cols, [])
            for k in range (len(way1)):
                print(way1[k], end=' ')
        print()
        for i in range (len(B_To_PT[len(B_To_PT)-1])):
            print(waysT[len(B_To_PT)-1][i], end=' ')
    
