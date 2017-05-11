# Prometheus was punished by the gods for giving the gift of
#  knowledge to man. He was cast into the bowels of the earth
#  and pecked by birds.

start = [[0,1,0,1,0,1,0,1],
         [1,0,1,0,1,0,1,0],
         [0,1,0,1,0,0,0,1],
         [0,0,0,0,2,0,0,0],
         [0,0,0,10,0,0,0,0],
         [2,0,2,0,2,0,2,0],
         [0,2,0,2,0,2,0,0],
         [2,0,2,0,2,0,0,0]]

alt = [[0,0,0,0,0,0,0,1],
       [0,0,0,0,1,0,1,0],
       [0,1,0,0,0,1,0,1],
       [1,0,1,0,1,0,0,0],
       [0,0,0,2,0,0,0,2],
       [1,0,0,0,2,0,2,0],
       [0,2,0,2,0,2,0,1],
       [0,0,0,0,0,0,0,0]]

def findOptimalMove(y,x,board,king,dbJump=0,moveList=[],recursion_check=0): # If dbJump == 1, then it must return either a jump or nothing
    score = 0
    if recursion_check > 4: return 0
    moveList = [(y,x)] # Start a new sequence
    dirs = [(1,1),(1,-1),(-1,1),(-1,-1)] if king else [(1,1),(1,-1)]
    maxScore = -1
    for (dy,dx) in dirs:
        if y+dy in range(8) and x+dx in range(8):
            if board[y+dy][x+dx]:
                if y+dy*2 in range(8) and x+dx*2 in range(8) and not board[y+dy*2][x+dx*2] and board[y+dy][x+dx] % 9 == 2:
                    score = 1
                    # Jump, and check for another jump
                    secondMove = findOptimalMove(y+dy*2,x+dx*2,board,king,1,moveList,recursion_check+1) # Check for double-jump
                    if secondMove:
                        score += secondMove[1]
                        if score > maxScore:
                            maxScore = score
                            moveList = [(y,x)] + secondMove[0] # Make double-jump if possible
                    else:
                        if score > maxScore:
                            maxScore = score
                            moveList = [(y,x),(y+dy*2,x+dx*2)]
            elif not dbJump:
                score = 0
                if score > maxScore:
                    maxScore = score
                    moveList = [(y,x),(y+dy,x+dx)]
            else:
                return 0
    return [moveList,maxScore]
    # Returns best move for a piece, and its score

def makeMove(board):
    possibleMoves = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 1 or cell == 10:
                possibleMoves += [findOptimalMove(y,x,board,cell==10)]
    # Decides best move
    possibleScores = [x[1] for x in possibleMoves]
    bestIndex = possibleScores.index(max(possibleScores))
    bestMove = possibleMoves[bestIndex]
    formattedBest = [(x,y) for (y,x) in bestMove[0]]
    return formattedBest

print(makeMove(start))
