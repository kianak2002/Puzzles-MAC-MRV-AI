import numpy as np
'''
class for node to save robot and butter for each node
and saves th parent and action from parent for the path
'''
class node():
    def __init__(self, parent, robot, butter, action_from_par):
        self.parent = parent
        self.robot = robot
        self.butter = butter
        self.action_from_par = action_from_par


'''
class for map and finding robot and butters and plates and obstacles position
and check the available actions for both normal and reversed movements 
'''


class environment():
    def __init__(self, map_file):
        self.rows, self.cols = map(int, map_file.readline().split())
        self.table = [map_file.readline().split() for j in range(self.rows)]
        self.find_people()
        self.find_butter()
    '''
    to have the plates and butters position and table and cols
    '''
    def map(self):
        return self.people_list, self.butter_list, self.table, self.cols

    '''
    to find plates(people) position
    '''
    def find_people(self):
        self.people_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'p' in self.table[i][j]:
                    self.people_list.append((i, j))

    '''
    to find robot position
    '''
    def find_robot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if 'r' in self.table[i][j]:
                    return i, j
    '''
    to find the butters position
    '''
    def find_butter(self):
        self.butter_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'b' in self.table[i][j]:
                    self.butter_list.append((i, j))
    '''
    to find the obstacles position
    '''
    def find_obstacles(self):
        self.obstacle_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'x' in self.table[i][j]:
                    self.obstacle_list.append((i, j))
    '''
    check all the available actions for robot and return them
    '''
    def available_actions(self, robot, butter):
        actions = []
        if robot[0] - 1 >= 0 and self.table[robot[0] - 1][robot[1]] != "x":
            if butter == (robot[0] - 1, robot[1]):
                if robot[0] - 2 >= 0 and self.table[robot[0] - 2][robot[1]] != "x":
                    actions.append("U")
            else:
                actions.append("U")

        if robot[0] + 1 < self.rows and self.table[robot[0] + 1][robot[1]] != "x":
            if butter == (robot[0] + 1, robot[1]):
                if robot[0] + 2 < self.rows and self.table[robot[0] + 2][robot[1]] != "x":
                    actions.append("D")
            else:
                actions.append("D")

        if robot[1] - 1 >= 0 and self.table[robot[0]][robot[1] - 1] != "x":
            if butter == (robot[0], robot[1] - 1):
                if robot[1] - 2 >= 0 and self.table[robot[0]][robot[1] - 2] != "x":
                    actions.append("L")
            else:
                actions.append("L")

        if robot[1] + 1 < self.cols and self.table[robot[0]][robot[1] + 1] != "x":
            if butter == (robot[0], robot[1] + 1):
                if robot[1] + 2 < self.cols and self.table[robot[0]][robot[1] + 2] != "x":
                    actions.append("R")
            else:
                actions.append("R")
        return actions
    '''
    check the action given with all available actions
    if allowed then it moves the robot and if needed the butter
    '''
    def step(self, robot, butter, action):
        # action : "U", "D", "R", "L"
        # robot: tuple (x, y)
        if action not in self.available_actions(robot, butter):
            raise ValueError("action is not available")

        if action == "U":
            next_robot = robot[0] - 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0] - 1, butter[1]
            return next_robot, butter, int(cost)

        elif action == "D":
            next_robot = robot[0] + 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0] + 1, butter[1]
            return next_robot, butter, int(cost)

        elif action == "L":
            next_robot = robot[0], robot[1] - 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0], butter[1] - 1
            return next_robot, butter, int(cost)

        elif action == "R":
            next_robot = robot[0], robot[1] + 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            if next_robot == butter:
                butter = butter[0], butter[1] + 1
            return next_robot, butter, int(cost)

        else:
            raise ValueError("action is wrong")


'''
class for ids
it has the butter and robot and plates(people)
'''


class agent():
    def __init__(self, env):
        self.env = env
        self.butter = env.find_butter()
        self.robot = env.find_robot()
        self.people = env.find_people()
    '''
    ids algorithm 
    calls dfs for each depth
    '''
    def ids(self,people_list, butter, robot, table, cols):
        root = node(None, robot, butter, None)
        queue_temp=[]
        depth_limit = 20
        i = 0
        while (i<=depth_limit):
            front=[]
            res=self.dfs(root,front,i, people_list, table, cols, butter)
            if(res is not None):
                if   res[0] is not None and res[0] is not False:
                    res[0].insert(0, root)
                    return res[0],res[1],res[2],i

            i+=1
    '''
    recursive dfs algorithm
    '''
    def dfs(self,Node:node,path,depth, people_list, table,cols, first_butter):
        for person in people_list:
            if Node.butter == person:
                path, action_path, robot_last = self.show_path(Node, table, cols, first_butter)
                return path, action_path, robot_last
        if(depth<=0):
            return None,None,None
        next=[]
        actions = env.available_actions(Node.robot, Node.butter)
        for a in actions:
            next_robot, next_butter, _ = env.step(Node.robot, Node.butter, a)
            child = node(Node, next_robot, next_butter, a)
            next.append(child)
        for childs in next:
            res = self.dfs(childs,path,depth-1, people_list, table, cols, first_butter)
            if(res is not None):
                if res[0] is not None:
                    path.insert(0, childs)
                    return path,res[1],res[2]
    '''
    shows the path and also prints it
    '''
    def show_path(self, final_node, table, cols, butter):
        path = []
        action_path = []
        n = final_node
        print("****")
        while n.parent != None:
            path.append(n.robot)
            action_path.append(n.action_from_par)
            n = n.parent
        path.append(n.robot)
        path.reverse()
        action_path.reverse()
        print("path:", path)
        print("actions:", action_path)
        print("cost:", len(action_path))
        terminal(table, cols, path, action_path, butter)
        return action_path, path, final_node.robot

def beauty(table, cols):
    for i in range(len(table)):
        print(*table[i], sep='\t\t')


'''
to draw a map step by step
'''
def terminal(table, cols, path, action, butter):
    print()
    beauty(table, cols)
    print('------------------------------------------')
    xButter, yButter = butter[0], butter[1]
    check = False
    for i in range(1, len(action) + 1):
        table[path[i][0]][path[i][1]] += 'r'
        if path[i][0] == xButter and path[i][1] == yButter:
            check = True
            table[path[i][0]][path[i][1]] = table[path[i][0]][path[i][1]].replace('b', '')
        if action[i - 1] == 'U':
            table[path[i][0] + 1][path[i][1]] = table[path[i][0] + 1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0] - 1][path[i][1]] += 'b'
                xButter -= 1
        if action[i - 1] == 'D':
            table[path[i][0] - 1][path[i][1]] = table[path[i][0] - 1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0] + 1][path[i][1]] += 'b'
                xButter += 1
        if action[i - 1] == 'R':
            table[path[i][0]][path[i][1] - 1] = table[path[i][0]][path[i][1] - 1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] + 1] += 'b'
                yButter += 1
        if action[i - 1] == 'L':
            table[path[i][0]][path[i][1] + 1] = table[path[i][0]][path[i][1] + 1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] - 1] += 'b'
                yButter -= 1
        check = False
        beauty(table, cols)
        print('--------------------------------------')

if __name__ == "__main__":
    with open("test3.txt", "r") as file:
        env = environment(file)
    people_list, butter_list , table, cols = env.map()
    robot = env.find_robot()
    test_agent = agent(env)
    for i in range(len(butter_list)):
        res = test_agent.ids(people_list, butter_list[i], robot, table, cols)
        robot = res[2]
        if res[3] == 0:
            print("Impossible!")
            print("path:", [])
            print("actions:", [])
            print("cost:", res[3])
        print("goal depth:", res[3])
