# import numpy as np
# import math

class Node:

    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        self.g = 0  # cost from start
        self.h = 0  # avg cost to goal
        self.f = 0  # g + h

    def __eq__(self, other):
        return (self.pos[0] == other.pos[0]) and (self.pos[1] == other.pos[1])

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"{self.pos}, {self.f}"


def a_star_search(maze,start,end):
    start_node = Node(start, None)
    end_node = Node(end, None)
    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        open_list.sort()
        current_node = open_list.pop(0)
        closed_list.append(current_node)
        if current_node == end_node:
            path = []
            while current_node != start_node:
                path.append(current_node.pos)
                current_node = current_node.parent
            return path[::-1]
        (x,y) = current_node.pos
        x,y = int(x),int(y)
        neighbors = [[x + 1, y],[x - 1, y],[x, y + 1],[x, y - 1]]

        for neighbor in neighbors:
            grid_cost = maze[neighbor[1]][neighbor[0]]
            new_node = Node(neighbor, current_node)
            if grid_cost == -1:
                continue

            if new_node in closed_list:
                continue
            new_node.g = current_node.g + grid_cost
            new_node.h = manhattan_distance(new_node.pos, end_node.pos)
            new_node.f = new_node.g + new_node.h

            if add_to_open(open_list, new_node):
                open_list.append(new_node)
    return None


def add_to_open(open_list, new_node):
    for node in open_list:
        if node == new_node and node.f >= new_node.f:
            return False
    return True

def manhattan_distance(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    return 5 * (abs(x1 - x2) + abs(y1 - y2))


