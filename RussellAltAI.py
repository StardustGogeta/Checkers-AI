from CheckersFunctions import *
from random import choice



def alt_simple_ai(board):
    moves = [AltMove(coords) for coords in get_moves(board)]

    for m in moves:
        m.set_features(board)
        m.set_advanced_features(board)
        m.set_value()

    best_value = max([m.value for m in moves])
    best_moves = [m for m in moves if m.value == best_value]
    chosen_move = choice(best_moves)
    # print "making move of value: " + str(chosen_move.value)
    return chosen_move.coords




alt_value_set = {
    "rank up": 1,
    "jump": 3,
    "king jump": 5,
    "king me": 5,
    "open back": -2
}

alt_advanced_value_set = {
    "threatened": -1,
    "seeking": 3,
    "forethought": 1            # Dynamic
}


class AltMove:
    def __init__(self, coords):
        self.coords = coords
        
        self.value = 0
        
        self.features = dict([(key, False) for key in alt_value_set.keys()])
        self.advanced_features = dict([(key, False) for key in alt_advanced_value_set.keys()])


    def set_features(self, board):
        start = self.coords[0]
        end  = self.coords[-1]
        second = self.coords[1]

        if end[1] - start[1] == 1:
            self.features["rank up"] = True

        if abs(start[1] - second[1]) >= 2:
            self.features["jump"] = len(self.coords) - 1
            for i in range(len(self.coords) - 1):
                start_ = self.coords[i]
                end_ = self.coords[i + 1]
                jumped = board[(start_[1] + end_[1]) // 2][(start_[0] + end_[0]) // 2]
                if jumped == 2:
                    self.features["jump"] += 1
                elif jumped == 20:
                    self.features["king jump"] += 1

        if end[1] == 7:
            self.features["king me"] = True

        if start[1] == 0:
            self.features["open back"] = True


    def set_advanced_features(self, board):
        start = self.coords[0]
        end  = self.coords[-1]

        if end[0] not in (0, 7):
            for x_shift in (-1, 1):
                try:
                    if board[end[1] + 1][end[0] + x_shift] in (2, 20):
                        self.advanced_features["threatened"] = True
                except:
                    pass

        if board[start[1]][start[0]] == 10:
            com = [0, 0]
            count = 0
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] in (2, 20):
                        com[0] += x
                        com[1] += y
                        count += 1
            com[0] /= count
            com[1] /= count
            self.advanced_features["seeking"] = (end[1] - com[1])**2 + (end[0] - com[0])**2 < (start[1] - com[1])**2 + (start[0] - com[0])**2
            # print "SEEKING"

    def set_value(self):
        for key in self.features.keys():
            self.value += alt_value_set[key] * self.features[key]
        for key in self.advanced_features.keys():
            if self.advanced_features[key]:
                self.value += alt_advanced_value_set[key]
