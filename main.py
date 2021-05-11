import numpy as np


class node():
    def __init__(self, parent, robot, butter, action_from_par):
        self.parent = parent
        self.robot = robot
        self.butter = butter
        self.action_from_par = action_from_par


class environment():
    def __init__(self, map_file):
        self.rows, self.cols = map(int, map_file.readline().split())
        self.table = [map_file.readline().split() for j in range(self.rows)]
        self.find_people()
        self.find_butter()

    def map(self):
        return self.people_list, self.butter_list

    def find_people(self):
        self.people_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'p' in self.table[i][j]:
                    self.people_list.append((i, j))

    def find_robot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if 'r' in self.table[i][j]:
                    return i, j

    def find_butter(self):
        self.butter_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'b' in self.table[i][j]:
                    self.butter_list.append((i, j))

    def find_obstables(self):
        self.obstacle_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if 'x' in self.table[i][j]:
                    self.obstacle_list.append((i, j))

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

    def available_actions_reverse(self, robot, butter):
        actions = []
        if robot[0] - 1 >= 0 and self.table[robot[0] - 1][robot[1]] != "x":
            if butter != (robot[0] - 1, robot[1]):
                actions.append("U")

        if robot[0] + 1 < self.rows and self.table[robot[0] + 1][robot[1]] != "x":
            if butter != (robot[0] + 1, robot[1]):
                actions.append("D")

        if robot[1] - 1 >= 0 and self.table[robot[0]][robot[1] - 1] != "x":
            if butter != (robot[0], robot[1] - 1):
                actions.append("L")

        if robot[1] + 1 < self.cols and self.table[robot[0]][robot[1] + 1] != "x":
            if butter != (robot[0], robot[1] + 1):
                actions.append("R")

        return actions

    def step_inverse(self, robot, butter, action):
        # action : "U", "D", "R", "L"
        # robot: tuple (x, y)
        if action not in self.available_actions_reverse(robot, butter):
            raise ValueError("action is not available")

        if action == "U":
            next_robot = robot[0] - 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_D = robot[0] + 1, robot[1]
            if butter == robot_D:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "D":
            next_robot = robot[0] + 1, robot[1]
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_U = robot[0] - 1, robot[1]
            if butter == robot_U:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "L":
            next_robot = robot[0], robot[1] - 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_R = robot[0], robot[1] + 1
            if butter == robot_R:
                butter = robot
            return next_robot, butter, int(cost)

        elif action == "R":
            next_robot = robot[0], robot[1] + 1
            cost = self.table[next_robot[0]][next_robot[1]]
            cost = cost.replace("b", "")
            cost = cost.replace("r", "")
            cost = cost.replace("p", "")
            robot_L = robot[0], robot[1] - 1
            if butter == robot_L:
                butter = robot
            return next_robot, butter, int(cost)

        else:
            raise ValueError("action is wrong")


class agent():
    def __init__(self, env):
        self.env = env
        self.butter = env.find_butter()
        self.robot = env.find_robot()
        self.people = env.find_people()

    def bfs(self):
        queue = []
        root = node(None, self.robot, self.butter, None)
        queue.append(root)
        while True:
            n = queue.pop(0)
            if n.butter == self.people:
                self.show_path(n)
                break
            actions = env.available_actions(n.robot, n.butter)
            for a in actions:
                next_robot, next_butter, _ = env.step(n.robot, n.butter, a)
                child = node(n, next_robot, next_butter, a)
                queue.append(child)

    def bidirectional_bfs(self, people_list, butter, robot):
        queue_r = []
        queue_p = []
        is_visited_r = {}
        is_visited_p = {}
        root_r = node(None, robot, butter, None)
        queue_r.append(root_r)


        for i in range(len(people_list)):
            actions = env.available_actions(people_list[i], people_list[i])
            for a in actions:
                next_robot, next_butter, _ = env.step(people_list[i], people_list[i], a)
                child = node(None, robot=next_robot, butter=people_list[i], action_from_par=None)
                queue_p.append(child)

        while True:
            node_r = queue_r.pop(0)
            node_p = queue_p.pop(0)
            is_visited_r[node_r.robot + node_r.butter] = node_r
            is_visited_p[node_p.robot + node_p.butter] = node_p
            # print(node_r.robot, node_r.butter, node_r.action_from_par, node_p.robot, node_p.butter, node_p.action_from_par)
            if node_r.robot + node_r.butter in is_visited_p.keys():
                self.show_bidirectional_path(node_r, is_visited_p[node_r.robot + node_r.butter])
                n = is_visited_p[node_r.robot + node_r.butter]
                while n.parent != None:
                    n = n.parent
                return n.butter
                # break
            if node_p.robot + node_p.butter in is_visited_r.keys():
                self.show_bidirectional_path(is_visited_r[node_p.robot + node_p.butter], node_p)
                n = node_p
                while n.parent != None:
                    n = n.parent
                return n.butter
                # break
            actions = env.available_actions(node_r.robot, node_r.butter)
            for a in actions:
                next_robot, next_butter, _ = env.step(node_r.robot, node_r.butter, a)
                if next_robot + next_butter not in is_visited_r.keys():
                    child = node(node_r, next_robot, next_butter, a)
                    queue_r.append(child)

            actions = env.available_actions_reverse(robot=node_p.robot, butter=node_p.butter)
            for a in actions:
                next_robot, next_butter, _ = env.step_inverse(robot=node_p.robot, butter=node_p.butter, action=a)
                if next_robot + next_butter not in is_visited_p.keys():
                    child = node(node_p, next_robot, next_butter, a)
                    queue_p.append(child)

    def show_path(self, final_node):
        n = final_node
        print("****")
        print(n.robot, n.action_from_par)
        while n != None:
            n = n.parent
            print(n.robot, n.action_from_par)

    def show_bidirectional_path(self, final_node_r, final_node_p):
        n = final_node_r
        print("****")
        print(n.robot, n.butter, n.action_from_par)
        while n.parent != None:
            n = n.parent
            print(n.robot, n.butter, n.action_from_par)

        n = final_node_p
        print(n.robot, n.butter, n.action_from_par)
        while n.parent != None:
            n = n.parent
            print(n.robot, n.butter, n.action_from_par)

    def inv(self, action):
        if action == "U":
            return "D"
        if action == "D":
            return "U"
        if action == "R":
            return "L"
        if action == "L":
            return "R"


if __name__ == "__main__":
    with open("test3.txt", "r") as file:
        env = environment(file)
    people_list, butter_list = env.map()
    robot = env.find_robot()
    print(people_list, butter_list)
    test_agent = agent(env)
    print(len(butter_list))
    for i in range(len(butter_list)):
        # print(robot)
        robot = test_agent.bidirectional_bfs(people_list, butter_list[i], robot)
        print(robot)
    # test_agent.bidirectional_bfs()
