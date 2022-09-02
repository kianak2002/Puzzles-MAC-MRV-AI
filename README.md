***General Knowledge about Project

It fills the unsolved puzzles using backtracking algorithm (MRV) and forward checking and MAC.

*** Rules of the Filling the Puzzle
This puzzle has several rules {
1.	The numbers of 0s and 1s should be equal in each row and column)
2.	There should not be two same numbers right next to each other
3.	All sequences in rows and columns should be unique
}

*** Input and Output
![image](https://user-images.githubusercontent.com/61980014/188200440-4a4e1874-9b10-4752-b149-6f780f89c7b6.png)



***How it is implemented

from collections import defaultdict
import copy

'''
a class for node
we save the f,g,h and parent and position for each node
'''


class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.robot_path = []
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


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
        self.robot = self.find_robot()

    '''
    to have the plates and butters and position and the map and columns
    '''

    def map(self):
        return self.cols, self.table, self.people_list, self.butter_list, self.robot

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
find the correct path for butter
we call the A_star_again so that it gives path for robot
'''


def A_star(start, end, table, cols, robot, robot_paths, parents, for_robot=False):
    maze = table
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)

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
                path.append((current.position, current.robot_path))
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # check if the movement is available
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # check if it goes into obstacle
            if maze[node_position[0]][node_position[1]] == 'x':
                continue
            new_node = Node(current_node, node_position)
            parents[new_node.position] = current_node.position
            children.append(new_node)

        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            if 'r' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('r', ''))
            elif 'b' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('b', ''))
            elif 'p' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('p', ''))
            else:
                child.g = current_node.g + int(maze[int(child.position[0])][int(child.position[1])])

            if for_robot is False:
                current = current_node.position  # Where the butter is
                next = child.position  # Where the butter is gonna go
                dx = next[0] - current[0]
                dy = next[1] - current[1]
                previous = (
                current[0] - dx, current[1] - dy)  # Where we want the robot to go, so it can push the butter
                parent = parents[child.position]
                robot_loc = None
                try:
                    robot_loc = robot_paths[parent][-1][0]
                except:
                    robot_loc = robot

                # Check obstacles and if it is in range
                if 0 <= previous[0] < len(table) and 0 <= previous[1] < len(table[1]) and table[previous[0]][
                    previous[1]] != 'x':
                    table_new = copy.deepcopy(table)
                    table_new[current[0]][current[1]] = 'x'
                    robot_path = A_star_again(robot_loc, previous, table_new)

                    robot_path += [(current_node.position, [])]  # push

                    child.robot_path = robot_path
                    robot_paths[child.position] = robot_path

            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            if for_robot or (child.position in robot_paths.keys()):
                open_list.append(child)

    return []


'''
find the correct path for robot based on the path for butter
'''


def A_star_again(start, end, table):
    maze = table
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
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
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = Node()
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # check if it is within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # check if it doesnt go to obstacle
            if maze[node_position[0]][node_position[1]] == 'x':
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            if 'r' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('r', ''))
            elif 'b' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('b', ''))
            elif 'p' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = int(maze[int(child.position[0])][int(child.position[1])].replace('p', ''))
            else:
                child.g = current_node.g + int(maze[int(child.position[0])][int(child.position[1])])

            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


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
    for i in range (1, len(action)+1):
        print(table[path[i][0]][path[i][1]])
        table[path[i][0]][path[i][1]] += 'r'
        if path[i][0] == xButter and path[i][1] == yButter:
            check = True
            table[path[i][0]][path[i][1]] = table[path[i][0]][path[i][1]].replace('b', '')
        if action[i-1] == 'U':
            table[path[i][0]+1][path[i][1]] = table[path[i][0]+1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0]-1][path[i][1]] += 'b'
                xButter -= 1
        if action[i-1] == 'D':
            table[path[i][0]-1][path[i][1]] = table[path[i][0]-1][path[i][1]].replace('r', '')
            if check:
                table[path[i][0]+1][path[i][1]] += 'b'
                xButter +=1
        if action[i-1] == 'R':
            table[path[i][0]][path[i][1]-1] = table[path[i][0]][path[i][1]-1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] + 1] += 'b'
                yButter +=1
        if action[i-1] == 'L':
            table[path[i][0]][path[i][1]+1] = table[path[i][0]][path[i][1]+1].replace('r', '')
            if check:
                table[path[i][0]][path[i][1] - 1] += 'b'
                yButter -= 1
        check = False
        beauty(table, cols)
        print('--------------------------------------')


'''
gets the butters and plates positions 
we give the first butter from list to the first plate on list and second to second and ...
call the A star and gets the path and calculate the cost based on the path
print path and actions and cost and goal depth
'''


def main():
    with open("test3.txt", "r") as file:
        env = environment(file)
    cols, table, people, butters, robot = env.map()
    all_path = []
    for i in range(len(butters)):
        actions = []
        butter = butters[i]
        person = people[i]
        cheat_path = []
        robot_paths = {}
        parents = {}
        cost = 0

        path = A_star(butter, person, table, cols, robot, robot_paths, parents)
        all_path.append(path)
        ##if there is no way !
        if all_path == [[]]:
            print("NO WAY!")
            continue

        robot = path[-1][-1][-1][0]  ##update the robot location
        print(f'Butter From {butter} to {person} goes like:')
        last = None
        for sec in path:
            for i in range(len(sec[1]) - 1):
                compare_x = sec[1][i][0]
                compare_y = sec[1][i][1]
                if i == len(sec[1]) - 2:
                    compared_x = sec[1][i + 1][0][0]
                    compared_y = sec[1][i + 1][0][1]
                else:
                    compared_x = sec[1][i + 1][0]
                    compared_y = sec[1][i + 1][1]
                if last != (compare_x, compare_y):
                    cheat_path.append((compare_x, compare_y))
                if i == len(sec[1]) - 2:
                    cheat_path.append((compared_x, compared_y))
                if compare_x - compared_x == 0:
                    if compare_y - compared_y == 1:
                        actions.append("L")
                    elif compare_y - compared_y == -1:
                        actions.append("R")
                elif compare_y - compared_y == 0:
                    if compare_x - compared_x == 1:
                        actions.append("U")
                    elif compare_x - compared_x == -1:
                        actions.append("D")
                last = cheat_path[-1]
        print("path:", cheat_path)
        print(actions)
        print("goal depth:", len(actions))
        for j in range(len(cheat_path)):
            if 'r' in table[cheat_path[j][0]][cheat_path[j][1]]:
                cost += int(table[cheat_path[j][0]][cheat_path[j][1]].replace('r', ''))
            elif 'b' in table[cheat_path[j][0]][cheat_path[j][1]]:
                cost += int(table[cheat_path[j][0]][cheat_path[j][1]].replace('b', ''))
            elif 'p' in table[cheat_path[j][0]][cheat_path[j][1]]:
                cost += int(table[cheat_path[j][0]][cheat_path[j][1]].replace('p', ''))
            else:
                cost += int(table[cheat_path[j][0]][cheat_path[j][1]])
        print("cost:", cost)
        table_help = copy.deepcopy(table)
        terminal(table_help, cols, cheat_path, actions, butter)
        del table_help


if __name__ == '__main__':
    main()
