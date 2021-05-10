from collections import defaultdict
import copy

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.robot_path = []

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class environment():
    def __init__(self, map_file):
        self.rows, self.cols = map(int, map_file.readline().split())
        self.table = [map_file.readline().split() for j in range(self.rows)]

        self.find_people()
        self.find_butter()
        self.robot = self.find_robot()

    def map(self):
        return self.cols, self.table, self.people_list, self.butter_list, self.robot

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


def input(address):
    text = open(address, "r")
    rows, cols = map(int, text.readline().split())
    table = [text.readline().split() for j in range(rows)]
    print(table)
    return table, cols


'''
find the path from r to all the butters!! and print the path
'''

def A_star(start, end, table, cols, robot, robot_paths, parents, for_robot=False):
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
                path.append((current.position, current.robot_path))
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 'x':
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            parents[new_node.position] = current_node.position
            children.append(new_node)

            # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            if 'r' in maze[int(child.position[0])][int(child.position[1])] or 'b' in maze[int(child.position[0])][
                int(child.position[1])] \
                    or 'p' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = 0
            else:
                child.g = current_node.g + int(maze[int(child.position[0])][int(child.position[1])])

            if for_robot is False:
                current = current_node.position  # Where we are
                next = child.position  # Where we wanna go

                dx = next[0] - current[0]
                dy = next[1] - current[1]
                previous = (current[0] - dx, current[1] - dy)  # Where we want the robot to go, so it can push us

                parent = parents[child.position]
                robot_loc = None
                try:
                    robot_loc = robot_paths[parent][-1][0]
                except:
                    robot_loc = robot

                # Check bounds and obstacles
                if 0 <= previous[0] < len(table) and 0 <= previous[1] < len(table[1]) and table[previous[0]][
                    previous[1]] != 'x':
                    table_new = copy.deepcopy(table)
                    table_new[current[0]][current[1]] = 'x'
                    robot_path = A_star_again(robot_loc, previous, table_new, cols)
                    # robot_path = A_star(robot_loc, previous, table, cols, robot, {}, {}, for_robot=True)
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



def A_star_again(start, end, table, cols):
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
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

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
            if child in closed_list:
                continue

            # Create the f, g, and h values
            if 'r' in maze[int(child.position[0])][int(child.position[1])] or 'b' in maze[int(child.position[0])][
                int(child.position[1])] \
                    or 'p' in maze[int(child.position[0])][int(child.position[1])]:
                child.g = 0
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

def main():
    with open("test3.txt", "r") as file:
        env = environment(file)
    cols, table, people, butters, robot = env.map()
    print(cols, table)
    all_path = []
    for i in range(len(butters)):
        actions = []
        butter = butters[i]
        person = people[i]

        robot_paths = {}
        parents = {}

        path = A_star(butter, person, table, cols, robot, robot_paths, parents)
        all_path.append(path)
        robot = path[-1][-1][-1][0] ##update the robot location

        print(f'From {butter} to {person} goes like:')
        for sec in path:
            for i in range(len(sec[1]) - 1):
                compare_x = sec[1][i][0]
                compare_y = sec[1][i][1]
                if i == len(sec[1]) - 2:
                    compared_x = sec[1][i + 1][0][0]
                    compared_y = sec[1][i + 1][0][1]
                else:
                    compared_x = sec[1][i+1][0]
                    compared_y = sec[1][i + 1][1]
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
        print(actions)

if __name__ == '__main__':
    main()

