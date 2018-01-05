from itertools import combinations

from CheckersFunctions import *

class Ai:
    def __init__(self, name, func):
        self.name = name
        self.func = func

        self.wins = 0
        self.losses = 0
        self.ties = 0

    def get_move(self, board):
        return self.func(board)



def flipped_board(board):
    # Rotate board
    new_board = [row[::-1] for row in board[::-1]]
    # switch 1's and 2's
    for y in range(len(new_board)):
        for x in range(len(new_board[y])):
            if new_board[y][x] == 1:
                new_board[y][x] = 2
            elif new_board[y][x] == 10:
                new_board[y][x] = 20
            elif new_board[y][x] == 2:
                new_board[y][x] = 1
            elif new_board[y][x] == 20:
                new_board[y][x] = 10
    return new_board


def display_board(board):
    legend = {0: ".", 1: "x", 10: "X", 2: "o", 20: "O"}
    print("\n".join([" ".join([legend[cell] for cell in row]) for row in board]))



def run_game(ai_a, ai_b):
    board = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0]
    ]

    # display_board(board)
    for i in range(MAX_TURNS):
        for ai in (ai_a, ai_b):
            # print "\n\n"

            if not has_moves(board):
                # display_board(board)
                return None
            
            move = ai.get_move(board)
            # print "\n\nmove: " + str(move)
            if is_legal_move(board, move):
                apply_move(board, move)
            else:
                print ("Illegal move made by " + ai.name, move)
                display_board(board)
                
            # if ai is ai_a:
            #     display_board(board)
            # else:
            #     display_board(flipped_board(board))

            board = flipped_board(board)

            if is_game_won(board):
                display_board(board)
                return ai

    print("MAX TURNS EXCEEDED")
    display_board(board)






def display_statistics(ais):
    print("==========================================================")
    print("||      Name      |   W   |   L   |   T   |    Score*   ||")
    print("||------------------------------------------------------||")
    for ai in sorted(ais, key=lambda ai: ai.score)[::-1]:
        print("||   " + "   |   ".join(str(x) for x in [(ai.name + " "*50)[:10], ai.wins, ai.losses, ai.ties, (" ", "  ")[ai.score >= 0.0] + str(ai.score) + (" ", "")[abs(ai.score) >= 10.0]]) + "    ||")
    print("==========================================================")
    print("\n* Score = W - L + T / 2")








if __name__ == "__main__":
    from Neptune import selectBestMove
    from Prometheus import makeMove
    from TestAIs import *
    from RussellAI import *
    from RussellAltAI import *

    MAX_TURNS = 1000
    
    ais = [
         Ai("Russell", simple_ai),
         Ai("Dark-Russell", alt_simple_ai),
         Ai("Prometheus", makeMove),
         Ai("Neptune", selectBestMove)
     ]

    # ais = [Ai("Russell " + str(x), simple_ai) for x in range(1, 6)]

    # ais = [Ai("Simple " + str(x), simple_ai) for x in range(1, 4)] + [Ai("AltSimple " + str(x), alt_simple_ai) for x in range(1, 4)]

    combs = combinations(ais, 2)

    for pair in combs:
        print(pair[0].name + " vs " + pair[1].name)
        victor = run_game(pair[0], pair[1])
        if victor is None:
            print("Stalemate!")
            for ai in pair: ai.ties += 1
        else:
            print(victor.name + " wins!")
            victor.wins += 1
            pair[pair[0] is victor].losses += 1
        print("\n")

    for ai in ais:
        ai.score = ai.wins - ai.losses + float(ai.ties) / 2.0

    display_statistics(ais)

