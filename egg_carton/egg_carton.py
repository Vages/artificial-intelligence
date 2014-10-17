__author__ = 'eirikvageskar'

from random import randrange
from copy import deepcopy
import numpy as np

#These functions assume that the boards are represented as numpy arrays

def array_dimensions(array):
    """Finds dimensions of array. Returns them in a tuple of form (width, height)

    :param array: An array
    :return: A tuple (width, height).
    """
    height = len(array)
    width = len(array[0])

    return width, height

def get_random_position(array, value):
    """Finds random position in 2D array with expected value.

    :param array: An array
    :param value: Wanted value
    :return: Coordinate in form (x, y)
    """
    if value not in array:
        raise ValueError(value, "Value not in array")
    else:
        height = len(array)
        width = len(array[0])
        while True:
            y = randrange(height)
            x = randrange(width)

            if array[y][x] == value:
                break

    return (x, y)


def add_egg(array):
    """Creates a new array with an egg added in a previously empty position.

    :param array: The old array
    :return: The new array
    """
    new_array = deepcopy(array)
    x, y = get_random_position(array, 0)
    new_array[y][x] = 1
    return new_array


def remove_egg(array):
    """Creates a new array with an empty position where there previously was an egg.

    :param array: The old array
    :return: The new array
    """
    new_array = deepcopy(array)
    x, y = get_random_position(array, 1)
    new_array[y][x] = 0
    return new_array


def move_egg(array):
    """Creates a new array with one egg moved from its previous position to an unoccupied one.

    :param array: The old array
    :return: The new array
    """
    new_array = deepcopy(array)
    old_x, old_y = get_random_position(array, 1)
    new_x, new_y = get_random_position(array, 0)
    new_array[old_y][old_x] = 0
    new_array[new_y][new_x] = 1
    return new_array


def array_sums(array):
    width, height = array_dimensions(array)
    vertical_sums = array.sum(0)
    horizontal_sums = array.sum(1)
    flipped_array = np.flipud(array)
    se_sums = []    # Sums in south-east-direction
    ne_sums = []    # Sums in north-est direction

    for i in range(-(height-1), width):
        se_sums.append(array.trace(i))

    for i in range(-(width-1), height):
        ne_sums.append(flipped_array.trace(i))

    return vertical_sums, horizontal_sums, se_sums, ne_sums


def evaluate_sums(sums, k, over_penal=1, under_penal=0.5):
    penal_sum = 0
    for list in sums:
        for elem in list:
            diff = k-elem
            if diff > 0:    # element is underweight
                penal_sum += diff*under_penal
            else:
                penal_sum += abs(diff)*over_penal

    return penal_sum


def generate_neighbors(array, funcs):
    neighbors = []
    for func in funcs:
        try:
            neighbors.append(func(array))
        except ValueError as e:
            pass

    return neighbors



def first_test():
    test_array = np.array([ [1, 0, 1, 0, 0],
                            [0, 1, 0, 0, 1],
                            [0, 1, 0, 1, 0],
                            [1, 0, 0, 0, 1],
                            [0, 0, 1, 1, 0]])

    zero_array = np.zeros((5,5))
    one_array = np.ones((5,5))

    print(test_array)

    sums = array_sums(test_array)
    print(sums)
    value = evaluate_sums(sums, 2)
    print(value)
    print(evaluate_sums(array_sums(zero_array), 2))
    print(evaluate_sums(array_sums(one_array), 2))
    funcs = [add_egg, remove_egg, move_egg]
    print "null"
    print(generate_neighbors(zero_array, funcs))
    print "en"
    print(generate_neighbors(one_array, funcs))
    print "random"
    print(generate_neighbors(test_array, funcs))


if __name__ == "__main__":
    first_test()