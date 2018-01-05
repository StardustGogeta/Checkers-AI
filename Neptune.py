# A complete rewrite of the "Prometheus" checkers AI
import random
from CheckersFunctions import apply_move
# import copy

def IS_VAL_PLAYER(val):
        return val in (PLAYER, PLAYER_KING)

def IS_VAL_ENEMY(val):
        return val in (ENEMY, ENEMY_KING)

def display_board(board):
    legend = {0: ".", 1: "x", 10: "X", 2: "o", 20: "O"}
    return "\n".join([" ".join([legend[cell] for cell in row]) for row in board])

def flipBoard(board):
    new_board = [row[::-1] for row in board[::-1]]
    for y in range(8):
        for x in range(8):
            if new_board[y][x] == PLAYER:
                new_board[y][x] = ENEMY
            elif new_board[y][x] == PLAYER_KING:
                new_board[y][x] = ENEMY_KING
            elif new_board[y][x] == ENEMY:
                new_board[y][x] = PLAYER
            elif new_board[y][x] == ENEMY_KING:
                new_board[y][x] = PLAYER_KING
    return new_board

def reformat(move): # Switch x and y coordinates
    return [(x,y) for (y,x) in move]

# Play around with SAMPLE_SIZE and MAX_DEPTH (must be integers)
# 10 and 4 seem to be good values, with 3 and 3 being significantly worse but much faster
# Scoring is also easily editable, and is currently a simple point system
JUMPING_OPTIONAL = False
SAMPLE_SIZE = 10
MAX_DEPTH = 4 # CAREFUL: Exponential complexity
# The time complexity is, at a lower bound (ignoring captures), the number of possible moves ^ max_depth
# At an upper bound, sample_size ^ max_depth

# Space values in array (enemy must be 2x player value for scoring to work properly)
EMPTY = 0
PLAYER = 1
ENEMY = 2
PLAYER_KING = 10
ENEMY_KING = 20

# The starting checkers position.
start = [   [0,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0],
                 [0,1,0,1,0,1,0,1],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [2,0,2,0,2,0,2,0],
                 [0,2,0,2,0,2,0,2],
                 [2,0,2,0,2,0,2,0]   ]

# Some test boards to try out
easy = [   [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,1,0,0,0,0],
                 [0,0,2,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0]   ]

easy2 = [   [0,0,0,0,0,0,0,0],
                 [0,0,0,0,1,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,2,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0]   ]

moderate = [   [0,0,0,0  ,0,0,0,0],
                         [2,0,2,0  ,0,0,0,0],
                         [0,0,0,10,0,0,0,0],
                         [0,0,2,0  ,2,2,0,0],
                         [0,0,0,0  ,0,0,0,0],
                         [0,0,2,0  ,2,0,2,0],
                         [0,0,0,0  ,0,0,0,0],
                         [0,0,0,0  ,0,0,0,0]   ]

moderate2 =  [   [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,1,0,1,0,0,0,0],
                             [1,0,2,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [1,0,2,0,0,0,0,0],
                             [0,2,0,2,0,0,0,0],
                             [0,0,2,0,0,0,0,0]   ]

##testBoard = [   [0,1,0,1,0,1,0,1],
##                 [1,0,1,0,1,0,1,0],
##                 [0,1,0,11,0,1,0,1],
##                 [0,0,2,0,2,0,0,0],
##                 [0,0,0,0,0,0,0,0],
##                 [2,0,2,0,2,0,2,0],
##                 [0,0,0,0,0,0,0,2],
##                 [2,0,0,0,2,0,2,0]   ]
# Should have the following possible moves (jumping not optional)
# [[(2, 1), (3, 0)], [(2, 1), (4, 3), (6, 1)], [(2, 1), (4, 3), (6, 5)], [(2, 3), (4, 1), (6, 3), (4, 5), (2, 3)],
# [(2, 3), (4, 5), (6, 3), (4, 1), (2, 3)], [(2, 5), (3, 6)], [(2, 5), (4, 3), (6, 1)], [(2, 5), (4, 3), (6, 5)], [(2, 7), (3, 6)]]
# With optional jumping:
# [[(2, 1), (3, 0)], [(2, 1), (4, 3), (6, 1)], [(2, 1), (4, 3), (6, 5)], [(2, 1), (4, 3)],
# [(2, 3), (4, 1), (6, 3), (4, 5), (2, 3)], [(2, 3), (4, 1), (6, 3), (4, 5)], [(2, 3), (4, 1), (6, 3)],
# [(2, 3), (4, 1)], [(2, 3), (4, 5), (6, 3), (4, 1), (2, 3)], [(2, 3), (4, 5), (6, 3), (4, 1)],
# [(2, 3), (4, 5), (6, 3)], [(2, 3), (4, 5)], [(2, 5), (3, 6)], [(2, 5), (4, 3), (6, 1)], [(2, 5), (4, 3), (6, 5)], [(2, 5), (4, 3)], [(2, 7), (3, 6)]]

# 0 is empty space
# 1 is player's pieces
# 11 is player's king
# 2 is enemy's pieces
# 12 is enemy's king

# I need to be able to move normally and recursively make infinite chains of captures
# Branch downwards
# If king, also branch upwards

# findMoves(board, y, x, piecesCaptured) -> list of possible moves (each move is a list of two-item tuples)
# When no moves are possible from the space, return []
# When a move is possible, return list of lists of tuples { ex. [[(3, 4), (4, 5)], [(3, 4), (2, 3)]] }
# board is game board
# y, x are coordinates
# piecesCaptured is list of coordinates of pieces captured

# Requirements:
# No repetitions allowed (recapturing same piece) However, repeated squares are OK!
# Work with recursion, in order to have infinite chains

def findMovesFromSpace(board, y, x, piecesCaptured, king, startPos, post_jump = False):
    def IS_PLAYER(Y,X):
        return board[Y][X] in (PLAYER, PLAYER_KING)
    def IS_ENEMY(Y,X):
        return board[Y][X] in (ENEMY, ENEMY_KING)
    moves = []
    
    if not post_jump:
        if x > 0 and y < 7 and board[y+1][x-1] == EMPTY: # Move D & L
            moves.append([(y+1, x-1)])
        if x < 7 and y < 7 and board[y+1][x+1] == EMPTY: # Move D & R
            moves.append([(y+1, x+1)])
    if x > 1 and y < 6:
        if ((y+2,x-2) == startPos or board[y+2][x-2] == EMPTY) and IS_ENEMY(y+1,x-1) and (y+1,x-1) not in piecesCaptured: # Jump D & L
            branches = findMovesFromSpace(board, y+2, x-2, piecesCaptured + [(y+1,x-1)], king, startPos, True)
            moves.extend(branches)
    if x < 6 and y < 6:
        if ((y+2,x+2) == startPos or board[y+2][x+2] == EMPTY) and IS_ENEMY(y+1,x+1) and (y+1,x+1) not in piecesCaptured: # Jump D & R
            branches = findMovesFromSpace(board, y+2, x+2, piecesCaptured + [(y+1,x+1)], king, startPos, True)
            moves.extend(branches)
    if king:
        if not post_jump:
            if x > 0 and y > 0 and board[y-1][x-1] == EMPTY: # Move U & L
                moves.append([(y-1, x-1)])
            if x < 7 and y > 0 and board[y-1][x+1] == EMPTY: # Move U & R
                moves.append([(y-1, x+1)])
        if x > 1 and y > 1:
            if ((y-2,x-2) == startPos or board[y-2][x-2] == EMPTY) and IS_ENEMY(y-1,x-1) and (y-1,x-1) not in piecesCaptured: # Jump U & L
                branches = findMovesFromSpace(board, y-2, x-2, piecesCaptured + [(y-1,x-1)], king, startPos, True)
                moves.extend(branches)
        if x < 6 and y > 1:
            if ((y-2,x+2) == startPos or board[y-2][x+2] == EMPTY) and IS_ENEMY(y-1,x+1) and (y-1,x+1) not in piecesCaptured: # Jump U & R
                branches = findMovesFromSpace(board, y-2, x+2, piecesCaptured + [(y-1,x+1)], king, startPos, True)
                moves.extend(branches)
    
    moves = [[(y, x)] + move for move in moves]
    if post_jump:
        if JUMPING_OPTIONAL:
            moves.append([(y,x)])
        if not moves:
            moves = [[(y, x)]]
    return moves
            

def getPossibleMoves(board):
    # Get all moves that are possible for the player
    moveList = []
    for y, row in enumerate(board):
        # Check if row contains player?
        for x, val in enumerate(row):
            if IS_VAL_PLAYER(val):
                moveList.extend(findMovesFromSpace(board, y, x, [], val == PLAYER_KING, (y,x)))
    return moveList

def analyzeBoard(board):
    combinedRows = [x for row in board for x in row]
    playerSum = sum(x for x in combinedRows if IS_VAL_PLAYER(x))
    enemySum = sum(x for x in combinedRows if IS_VAL_ENEMY(x)) / 2 # Enemy pieces must be 2x the value in the array
    if playerSum == 0: return -1000 # Lost
    if enemySum == 0: return 1000 # Won
    return playerSum-enemySum

def selectBestMove(board, recursion_depth = MAX_DEPTH, __verbose__ = False):
    possibleMoves = getPossibleMoves(board)
    if not possibleMoves: return -1000
    moveSubset = random.sample(possibleMoves, min(len(possibleMoves), SAMPLE_SIZE)) # Pick random moves from all possibilities
    assert recursion_depth > -1 # Prevent crashes

    moveSubsetVals = []
    if __verbose__: print(display_board(board))
    if not recursion_depth: # Base branch
        if __verbose__: print("base",moveSubset)
        for move in moveSubset:
            testBoard = [row[::] for row in board[::]] # Test against deepcopy
            apply_move(testBoard, reformat(move))
            boardVal = analyzeBoard(testBoard)
            moveSubsetVals.append(boardVal)
        if __verbose__: print("base",moveSubset,moveSubsetVals)
        return sum(moveSubsetVals) / len(moveSubsetVals) # Average of sample scores
    
    elif recursion_depth == MAX_DEPTH: # Top-level branch
        if __verbose__: print("top",moveSubset)
        for move in moveSubset:
            testBoard = [row[::] for row in board[::]] # Test against deepcopy
            apply_move(testBoard, reformat(move))
            boardVal = -selectBestMove(flipBoard(testBoard), recursion_depth-1) # Negate the score of the flipped board
            moveSubsetVals.append(boardVal)
        if __verbose__: print("top",moveSubset,moveSubsetVals)
        bestMove = moveSubset[moveSubsetVals.index(max(moveSubsetVals))]
        return reformat(bestMove)

    else: # Intermediate branch
        if __verbose__: print("int",moveSubset,recursion_depth)
        for move in moveSubset:
            testBoard = [row[::] for row in board[::]] # Test against deepcopy
            apply_move(testBoard, reformat(move))
            boardVal = -selectBestMove(flipBoard(testBoard), recursion_depth-1) # Negate the score of the flipped board
            moveSubsetVals.append(boardVal)
        if __verbose__: print("int",moveSubset,moveSubsetVals,recursion_depth)
        return sum(moveSubsetVals) / len(moveSubsetVals)

#print(findMovesFromSpace(testBoard, 2, 1, [], False, (2,1)))
#print(getPossibleMoves(testBoard))
#print(analyzeBoard(start))

# Adjacent pieces?
# Checking across small set of heuristics
# Playing against itself
# Incremental improvement (not too drastic)
