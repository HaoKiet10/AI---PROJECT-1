from copy import deepcopy

TIMEOUT = 10000


class state:
    def __init__(self, board, preState, path, weight, node, stonePos):
        self.board = board
        self.preState = preState
        self.weightPush = weight    # weight pushed
        self.node = node
        self.path = path
        self.stonePos = stonePos
        if path == None:
            self.steps = 0
        else:
            self.steps = len(path)


    def __lt__ (self, another):
        return self.weightPush < another.weightPush
    
    
def findPosition(board, weightStone):
    startPos = None
    stonePos = {}
    switchPos = set()
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "@":
                startPos = (i, j)
            if board[i][j] == "$" or board[i][j] == "*":
                stonePos[(i, j)] = weightStone[len(stonePos)]
            if board[i][j] == "." or board[i][j] == "*":
                switchPos.add((i, j))
    
    return startPos, stonePos, switchPos




def findPosAres(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "@" or board[i][j] == '+':
                return (i, j)

def nextDirections(board, curPos):     
    x, y = curPos[0], curPos[1]
    
    directions = []
    
    # Up: (x - 1, y)
    if 0 <= x - 1 < len(board):
        temp = board[x - 1][y]
        if temp == ' ' or temp == '.':
            directions.append((x - 1, y))
        elif temp == '$' or temp == '*' and 0 <= x - 2 < len(board): # TH: Push the stone.
            nextStone = board[x - 2][y]
            if nextStone != '#' and nextStone != '$' and nextStone != '*':
                directions.append((x - 1, y))
    
    
    # DOWN: (x + 1, y)
    if 0 <= x + 1 < len(board):
        temp = board[x + 1][y]
        if temp == ' ' or temp == '.':
            directions.append((x + 1, y))
        elif temp == '$' or temp == '*' and 0 <= x + 2 < len(board):
            nextStone = board[x + 2][y]
            if nextStone != '#' and nextStone != '$' and nextStone != '*':
                directions.append((x + 1, y))
                
    # LEFT: (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        temp = board[x][y - 1]
        if temp == ' ' or temp == '.':
            directions.append((x, y - 1))
        elif temp == '$' or temp == '*' and 0 <= y - 2 < len(board[0]):
            nextStone = board[x][y - 2]
            if nextStone != '#' and nextStone != '$' and nextStone != '*':
                directions.append((x, y - 1))
         
    # RIGHT: (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        temp = board[x][y + 1]
        if temp == ' ' or temp == '.':
            directions.append((x, y + 1))
        elif temp == '$' or temp == '*' and 0 <= y + 2 < len(board[0]):
            nextStone = board[x][y + 2]
            if nextStone != '#' and nextStone != '$' and nextStone != '*':
                directions.append((x, y + 1)) 
    
    return directions

def copyBoard(board):
    newBoard = []
    for i in range(len(board)):
        newBoard.append([])
        for j in range(len(board[0])):
            newBoard[i].append(board[i][j])
            
    return newBoard


def move(board, stonePos, nextPos, curPos, switchPos):
    newBoard = copyBoard(board)
    newStonePos = deepcopy(stonePos)
    
    if(newBoard[nextPos[0]][nextPos[1]] == '$' or newBoard[nextPos[0]][nextPos[1]] == '*'):
        x = 2 * nextPos[0] - curPos[0]
        y = 2 * nextPos[1] - curPos[1]
        
        # print("x and y: " + str(x) + str(y))
        # updated the position of Stone
        if (nextPos[0], nextPos[1]) in newStonePos:
            newStonePos[(x, y)] = newStonePos.pop((nextPos[0], nextPos[1]))
        
        if newBoard[x][y] == '.':
            newBoard[x][y] = '*'
        else:
            newBoard[x][y] = '$'
        
    if newBoard[nextPos[0]][nextPos[1]] == '*' or newBoard[nextPos[0]][nextPos[1]] == '.':
        newBoard[nextPos[0]][nextPos[1]] = '+'
    else:
        newBoard[nextPos[0]][nextPos[1]] = '@'
    
    if newBoard[curPos[0]][curPos[1]] == '+':
        newBoard[curPos[0]][curPos[1]] = '.'
    else:
        newBoard[curPos[0]][curPos[1]] = ' '

        
    for p in switchPos:
        if newBoard[p[0]][p[1]] == '*':
            continue
        elif newBoard[p[0]][p[1]] == ' ':
            newBoard[p[0]][p[1]] = '.'  
    
    
    return newBoard, newStonePos
    

def compareBoard(board1, board2):
    if not board1 or not board2:  
        return board1 == board2
    
    if len(board1) != len(board2) or len(board1[0]) != len(board2[0]):
        return False
    for i in range(len(board1)):
        for j in range(len(board1[0])):
            if board1[i][j] != board2[i][j]:
                return False
            
    return True

def checkSameBoard(board, listState):
    for state in listState:
        if compareBoard(board, state.board):
            return True
    return False
    
    
def checkWinner(board, switchPos):
    if board is None:
        print("Error: board is None")
        return False

    rows, cols = len(board), len(board[0])  

    for i in switchPos:
        if not (0 <= i[0] < rows and 0 <= i[1] < cols): 
            print(f"Invalid switch position: {i}")
            continue 
        
        if board[i[0]][i[1]] != '*':
            return False 
    return True


def moveDirection(board, nextPos, curPos):
    
    if nextPos[0] > curPos[0]:  # Down
        moveDirection = "d"
    elif nextPos[0] < curPos[0]:  # Up
        moveDirection = "u"
    elif nextPos[1] > curPos[1]:  # Right
        moveDirection = "r"
    elif nextPos[1] < curPos[1]:  # Left
        moveDirection = "l"
        
        
    if board[nextPos[0]][nextPos[1]] == '$':
        moveDirection = moveDirection.upper()
    
    return moveDirection

def checkWeight(board, stonePos, pos):
    if board[pos[0]][pos[1]] == '$' or board[pos[0]][pos[1]] == '*':
        # print("Position stone: " + str(pos[0]) + " " + str(pos[1]))
        if (pos[0], pos[1]) in stonePos:
            return stonePos[(pos[0], pos[1])]
        
    return 0


def printBoard(board, stonePos):
    
    with open('output.txt', 'a') as f: 
        f.write("-----------------\n")
        for row in board:
            f.write("\t".join(map(str, row)) + "\n")
        f.write(str(stonePos) + "\n")  
        

        
        
        
        