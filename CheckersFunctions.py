from copy import deepcopy

def is_legal_advance(board, init):
    start, end = init
    if board[start[1]][start[0]] == 1:
        return abs(end[0] - start[0]) == 1 and (end[1] - start[1] == 1)
    else:
        return abs(end[0] - start[0]) == 1 and abs(end[1] - start[1]) == 1


def is_legal_jump(board, init):
    start, end = init
    if board[(start[1] + end[1])//2][(start[0] + end[0])//2] in (2, 20):
        if board[start[1]][start[0]] == 1:
            if abs(end[0] - start[0]) == 2 and (end[1] - start[1] == 2):
                return True
            else:
                return False
        else:
            return abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 2
    else:
        return False



def is_legal_move(board, move):

    # Check for a null input
    if move is None:
        return False

    # If any square is off the board, return false
    if any(min(x, y) < 0 or max(x, y) > 7 for (x, y) in move):
        return False
    
    # If starting square is not an owned piece, return false
    if board[move[0][1]][move[0][0]] not in (1, 10):
        return False
    
    # If any intermediate square is occupied, return false
    if any(board[y][x] != 0 for (x, y) in move[1:]):
        return False

    # If move is a basic advance, check it
    if len(move) == 2 and abs(move[0][0] - move[1][0]) == 1:
        return is_legal_advance(board, move)

    # Check jump legality
    board_copy = deepcopy(board)
    for start, end in [(move[i], move[i+1]) for i in range(len(move) - 1)]:
        if not is_legal_jump(board_copy, [start, end]):
            return False
        apply_move(board_copy, [start, end])

    return True



def apply_move(board, move):
    start_value = board[move[0][1]][move[0][0]]
    board[move[0][1]][move[0][0]] = 0
    if len(move) == 2 and abs(move[0][0] - move[1][0]) == 1:
        board[move[1][1]][move[1][0]] = start_value
    else:
        for i in range(len(move) - 1):
            start = move[i]
            end = move[i + 1]
            board[(start[1] + end[1]) // 2][(start[0] + end[0]) // 2] = 0
        board[move[-1][1]][move[-1][0]] = start_value
    if move[-1][1] == 7:
        board[move[-1][1]][move[-1][0]] = 10



def has_moves(board):
    return len(get_moves(board)) > 0


def is_game_won(board):
    return sum([row.count(1) for row in board]) + sum([row.count(10) for row in board]) == 0



def get_jumps(board, open_, closed):
    # print "open_: ", open_
    new_open_ = deepcopy(open_)
    for move in open_:
        # print move
        current_move_changed = False
        last = move[-1]
        for shift_y in (-2, 2):
            for shift_x in (-2, 2):
                new = deepcopy(move)
                new.append((last[0] + shift_x, last[1] + shift_y))
                # print "checking new: " + str(new) 
                if is_legal_move(board, new):
                    current_move_changed = True
                    new_open_.append(new)    
        new_open_.remove(move)
        closed.append(move)

    if len(new_open_) == 0:
        return [move for move in closed if len(move) > 1]
    else:
        return get_jumps(board, new_open_, closed)



def get_moves(board):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] in (1, 10):
                for y_shift in (-1, 1):
                    for x_shift in (-1, 1):
                        if is_legal_move(board, [(x, y), (x + x_shift, y + y_shift)]):
                            moves.append([(x, y), (x + x_shift, y + y_shift)])
                moves.extend(get_jumps(board, [[(x, y)]], []))
    return moves




if __name__ == "__main__":

    board = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 1],
        [0, 0, 2, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0]
    ]

    print(get_moves(board))

    unit_tests = [
        ([(1, 2), (3, 4), (5, 6)], True),
        ([(1, 12), (2, 3)], False),
        ([(1, 2), (2, -3)], False),
        ([(1, 2), (2, 3), (3, 4)], False),
        ([(1, 4), (3, 2)], False),
        ([(1, 4), (3, 2), (5, 4)], False),
        ([(1, 2), (3, 4), (5, 6)], True),
        ([(1, 2), (3, 4), (5, 6), (3, 4)], False)
    ]

    for test in unit_tests:
        result = is_legal_move(board, test[0])
        print(str(test[0]) + " --> " + str(result) + "\t" + ("PASS" if result == test[1] else "FAIL"))
