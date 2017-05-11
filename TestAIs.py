from random import choice
from copy import deepcopy

from CheckersFunctions import *


def random_ai(board):
    return choice(get_moves(board))





if __name__ == "__main__":
    board = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0]
    ]

    # print get_moves(board)

    print(get_jumps(board, [[(1, 2)]], []))

    
