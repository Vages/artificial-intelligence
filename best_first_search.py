__author__ = 'eirikvageskar'

from heapq import heappush, heappop
from copy import deepcopy
from collections import deque

"""It is important to take note of the coordinate system.

First of all, the maps will consist of lists of lists. The x-axis will horizontal, directed to the right.
The y-axis will be vertical, directed downward. Both are 0-indexed.

Usually, the coordinates will be delivered in tuples of the form (x, y). When working with lists, it is therefore
necessary to swap the two, so that addressing the coordinate (a, b) on map c is done in the following way:
c[b][a]"""


class BoardError(Exception):
    """Error to be raised when board is unsolvable."""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def manhattan_distance(a, b):
    """Calculates the manhattan distance between two points (tuples).

    :param a: Starting point.
    :param b: Ending point.
    :return: Manhattan distance.
    """
    x = abs(b[0]-a[0])
    y = abs(b[1]-a[1])

    return x+y


def dijkstra_heur(*args):
    """Heuristic function for dijkstra

    :param args: anything
    :return: 0 in any case
    """
    return 0


def best_first_search(weight_map, start, goal, heur=manhattan_distance):
    """Does a best-first-search on the map using a given map of weight, start and goal coordinates.
    Uses manhattan distance as a standard heuristic function.

    :param goal: Goal coordinate (x, y).
    :param weight_map: List of lists of weights.
    :param start: Start coordinate (x, y).
    :param heur: Heuristic function. Manhattan distance as standard.
    :return:
    """


    cost = {start:0}

    '''Note: This algorithm takes advantage of the fact that the cost to each node is never relaxed if we always
    make sure to pop the node with the least cost from the queue. Therefore we have no need to propagate cost
    estimates
    '''

    inf = float('inf')  # Used for comparison

    offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))    # The four

    map_size_x = len(weight_map[0])    # Horizontal weight_map distance
    map_size_y = len(weight_map)       # Vertical weight_map distance

    pre = dict()    # Predecessor dicts
    pre[start] = None
    seen = set()    # The nodes that have been evaluated

    Q = [(cost[start]+heur(start, goal), start)]    # Push initial node onto heap (cost, (x, y))

    while Q:
        est, node = heappop(Q)
        if node in seen: continue   # Skip this iteration if the node has already been processed
        seen.add(node)
        if node == goal:
            return cost, pre, seen

        (a, b) = node

        for o in offsets:       # x coordinate
            i, j = o
            new_x, new_y = a+i, b+j
            new_node = (new_x, new_y)

            if (0 <= new_x < map_size_x) and (0 <= new_y < map_size_y) and (new_node not in pre):
                if weight_map[new_y][new_x] < inf:
                    pre[new_node] = node
                    new_node_cost = cost[node]+weight_map[new_y][new_x]    # Note swapped coordinates
                    cost[new_node] = new_node_cost
                    f = new_node_cost + heur(new_node, goal)
                    heappush(Q, (f, new_node))

    raise BoardError("No path from start to end")


def breadth_first_search(weight_map, start, goal):
    Q = deque()
    cost = {start:0}
    inf = float("inf")

    offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))

    map_size_x = len(weight_map[0])    # Horizontal weight_map distance
    map_size_y = len(weight_map)       # Vertical weight_map distance

    pre = dict()    # Predecessor dicts
    pre[start] = None
    seen = set()    # The nodes that have been evaluated

    Q.append(start)

    while Q:
        node = Q.popleft()

        if node in seen:
            continue
        seen.add(node)
        if node == goal:
            return cost, pre, seen

        (a, b) = node

        for o in offsets:
            i, j = o
            new_x, new_y = a+i, b+j
            new_node = (new_x, new_y)

            if (0 <= new_x < map_size_x) and (0 <= new_y < map_size_y) and (new_node not in pre):
                if weight_map[new_y][new_x] < inf:
                    pre[new_node] = node
                    new_node_cost = cost[node]+weight_map[new_y][new_x]    # Note swapped coordinates
                    cost[new_node] = new_node_cost
                    Q.append(new_node)

    raise BoardError("No path from start to end")




def process_board(board, trans_dict=None, start_char=("A", 1), goal_char=("B", 1)):
    """Translates a board from a string representation to a list, as well as finding start and goal positions.

    :param board: The board in a list of strings format.
    :param trans_dict: A dict linking characters to square costs
    :param start_char: A tuple of form (start character, cost).
    :param goal_char: A tuple of form (goal character, cost).
    :return: Tuple of form (processed board, start position, goal position).
    """
    size_y = len(board)
    size_x = len(board[0])

    finished = [[0]*size_x for y in range(size_y)]

    if trans_dict is None:
        trans_dict = {'.':1, '#':float("inf"), "r":1, "g":5, "f":10, "m":50, "w":100}

    trans_dict[start_char[0]]=start_char[1]
    trans_dict[goal_char[0]]=goal_char[1]
    for j in range(size_y):
        for i in range(size_x):
            char = board[j][i]
            if char == start_char[0]:
                start = (i, j)
            if char == goal_char[0]:
                goal = (i, j)
            finished[j][i] = trans_dict[char]

    return finished, start, goal


def file_to_stringlist(filepath):
    """Reads a board from a file to a list.

    :param filepath: The relative path to the file.
    :return: A list of lists of characters
    """

    a = open(filepath)
    list_thing = []
    for line in a:
        line = line.strip()     # Remove newline characters
        list_thing.append(list(line))

    return list_thing


def construct_predecessor_path(pre_dict, end):
    """Gives the shortest path to the endpoint.

    :param pre_dict: Predecessor dictionary
    :param end: The endpoint (starting point for algorithm).
    :return: A list of tuples representing the squares visited.
    """
    a = [end]

    while True:
        temp = pre_dict[a[-1]]
        if temp is None:
            break
        else:
            a.append(temp)

    a.reverse()

    return a


def fill_squares(char_map, coord_list, fill_character="o"):
    """Fills char_map squares given in coord_list with the given fill character.

    :param char_map: A char_map (coord_list of coord_list of characters)
    :param coord_list: Set of coordinates
    :param fill_character: Any character
    :return: The modified char_map
    """
    map_copy = deepcopy(char_map)

    for a, b in coord_list:
        map_copy[b][a] = fill_character

    return map_copy


def print_board(board):
    for line in board:
        print("".join(line))


#The following are solutions for tasks


def _task_a1_helper(board_path):
    string_board = file_to_stringlist(board_path)

    print("Before:")
    print_board(string_board)

    (board, start, goal) = process_board(string_board)

    cost, pre, seen = best_first_search(board, start, goal)

    path = construct_predecessor_path(pre, goal)

    mod_board = fill_squares(string_board, path, "o")

    print("\nAfter:")
    print_board(mod_board)


def _task_a2_helper(board_path):
    string_board = file_to_stringlist(board_path)

    print("Before:")
    print_board(string_board)

    (board, start, goal) = process_board(string_board)

    cost, pre, seen = best_first_search(board, start, goal)

    path = construct_predecessor_path(pre, goal)

    mod_board = fill_squares(string_board, path, ".")

    print("\nAfter:")
    print_board(mod_board)


def _task_a3_helper(board_path):
    pass

    #string_board = file_to_stringlist(board_path)



def task_a1():
    path = "boards/board-1-%d.txt"
    for i in range(1, 5):
        print("\nBoard 1-"+str(i))
        _task_a1_helper(path % (i))


def task_a2():
    path = "boards/board-2-%d.txt"
    for i in range(1, 5):
        print("\nBoard 2-"+str(i))
        _task_a2_helper(path % (i))



task_a1()
task_a2()

