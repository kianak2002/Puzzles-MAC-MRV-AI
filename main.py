import numpy as np
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
    to have the plates and butters position
    '''
    def map(self):
        return self.people_list, self.butter_list

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

class agent():
    def __init__(self, env):
        self.env = env
        self.butter = env.find_butter()
        self.robot = env.find_robot()
        self.people = env.find_people()

    def ids(self,people_list, butter, robot):
        root = node(None, robot, butter, None)
        queue_temp=[]
        depth_limit = 20
        i = 0
        while (i<=depth_limit):
            front=[]
            res=self.dfs(root,front,i, people_list)
            if res is not None and res is not False:
                res.insert(0, root)
                return res, i

            i+=1

    def dfs(self,Node:node,path,depth, people_list):
        for person in people_list:
            if Node.butter == person:
                path, action_path, robot_last = self.show_path(Node)
                return path, action_path, robot_last
        if(depth<=0):
            return None
        next = []
        actions = env.available_actions(Node.robot, Node.butter)
        for a in actions:
            next_robot, next_butter, _ = env.step(Node.robot, Node.butter, a)
            child = node(Node, next_robot, next_butter, a)
            next.append(child)
        for childs in next:
            res = self.dfs(childs,path,depth-1, people_list)
            if res is not None:
                path.insert(0, childs)
                return path



    def show_path(self, final_node):
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
        return action_path, path, n.robot


if __name__ == "__main__":
    with open("test3.txt", "r") as file:
        env = environment(file)
    people_list, butter_list = env.map()
    robot = env.find_robot()
    test_agent = agent(env)
    for i in range(len(butter_list)):
        res, i = test_agent.ids(people_list, butter_list[i], robot)
        print(robot)
        if i == 0:
            print("Impossible!")
            print("path:", [])
            print("actions:", [])
            print("cost:", i)
        print("goal depth:", i)

