import pygame
import os
from Move import drawBoard
from screenManager import switchToMove


# from main import readFile
# from supportFile import findPosition

BG_COLOR = (252, 248, 239)
BUTTON_COLOR = (100, 150, 255)
TEXT_COLOR = (255, 255, 255)
FRONT_SIZE = 36
SIZE = 50


width = 1000
height = 800

imageLeft = pygame.transform.scale(pygame.image.load("../Assets/left.png"), (SIZE, SIZE))
imageRight = pygame.transform.scale(pygame.image.load("../Assets/right.png"), (SIZE, SIZE))
imagePlay = pygame.transform.scale(pygame.image.load("../Assets/start.png"), (120, 100))
background = pygame.transform.scale(pygame.image.load("../Assets/background.png"), (width, height))

def readFile(inputFile):
    with open(inputFile, 'r') as file: 
        line = file.readlines()

    weightStone = list(map(int, line[0].strip().split()))  # get value and assign to list

    array_1D = []
    for line in line[1:]:
        if line.strip():
            array_1D.append(line.rstrip())

    array = [list(ch) for ch in array_1D] # convert 1D to 2D
    
    
    return  weightStone, array


def findPosition(board, weightStone):
    startPos = None
    stonePos = {}
    switchPos = set()
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "@":
                startPos = (i, j)
            elif board[i][j] == "$":
                stonePos[(i, j)] = weightStone[len(stonePos)]
            elif board[i][j] == ".":
                switchPos.add((i, j))
    
    return startPos, stonePos, switchPos


def drawText(screen, text, size):
    pygame.draw.rect(screen, (111, 187, 227, 255), (410, 140, 170, 60))
    # font = pygame.font.Font("comic sans ms", size)
    font = pygame.font.SysFont("comic sans ms", size)
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (425, 140))
    
def drawTitle(screen):
    pygame.draw.rect(screen, (237, 232, 220, 255), (0, 0, 1000, 50 ))
    font = pygame.font.Font(None, 70)
    title = font.render("SOKOBAN GAME", True, TEXT_COLOR)
    screen.blit(title, (300, 70))

def buttonChoice(screen):
    buttonLeft = pygame.Rect(350, 140, 60, 60)
    # pygame.draw.rect(screen, BUTTON_COLOR, buttonLeft)
    screen.blit(imageLeft, (355, 145))
    buttonRight = pygame.Rect(580, 140, 60, 60)
    # pygame.draw.rect(screen, BUTTON_COLOR, buttonRight)
    screen.blit(imageRight, (585, 145))
    
    return buttonLeft, buttonRight


def drawButtonPlay(screen, board):
    buttonPlay = pygame.Rect(450, len(board) * 50 + 300, 120, 100)
    # pygame.draw.rect(screen, (255, 255, 255), buttonPlay)
    screen.blit(imagePlay, (450, len(board) * 50 + 300))
    
    return buttonPlay

class algorithm:
    def __init__(self, algorithm, path, weight):
        self.algorithm = algorithm
        self.path = path 
        self.weight = weight
';./'
# get the data for UI
def readResult(filePath):
    result = {}
    algorithmList = []
    with open(filePath, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        
        
    
    for i in range(0, len(lines), 3):
        algori = lines[i].strip()
        path = lines[i + 1].strip()
        weight = int(lines[i + 2].strip())
        algorithmList.append(algori.lower())
        result[algori.lower()] = algorithm(algori, path, weight)
        
    return result , algorithmList

def drawButtonAlgorithm(screen, text):
    
    text = text.lower()
    dir = {"bfs" : "Breadth First Search", 
           "dfs" : "Depth First Search", 
           "ucs" : "Uniform Cost Search", 
           "astar" : "A Star",
           "aco" : "Swarm Intelligence"
    }
    # print("text: " + str(text))
    font = pygame.font.SysFont("comic sans ms", 25)
    temp = dir.get(text, "Select the algorithm")
    widText, heiText = font.size(temp)
    buttonAlgorithm = pygame.Rect(width/2 - widText/2 , 220, widText, heiText + 10)
    pygame.draw.rect(screen, (111, 187, 227, 255), buttonAlgorithm)
    
    label = font.render(temp, True, TEXT_COLOR)
    screen.blit(label, (width/2 - widText/2 , 220))
    
    return buttonAlgorithm


def drawListAlgorithm(screen, algorithmList):
    # algorithmList = ["BFS", "DFS", "UCS", "Astar"]
        
    running = True
    for  i in range(len(algorithmList)):
        algorithmList[i] = algorithmList[i].upper()
    while running:
        for i, algo in enumerate(algorithmList):  
            algoButton  = pygame.Rect(width // 2 - 100, height // 2 + i * 40 - 100, 200, 40)
            pygame.draw.rect(screen, (180, 180, 180), algoButton)
            font = pygame.font.SysFont("comic sans ms", 25)
            text = font.render(algo, True, (255, 255, 255))
            screen.blit(text, (width // 2 - 100 + 5 , height // 2 + i * 40 + 5 - 100, 195, 35))
        
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, algo in enumerate(algorithmList):
                        algoButton = pygame.Rect(width // 2 - 100, height // 2 + i * 40 - 100, 200, 40)
                        if algoButton.collidepoint(event.pos):
                                return algoButton, algo
       
def extractLevelNumber(filename):
    return int(filename.split('-')[1])               

def runHome(index, algo):
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban home")
    
    
    #  the list reversed
    folderPath = "../Data"
    fileList = sorted([f[:-4] for f in os.listdir(folderPath) if f.endswith(".txt")],key=extractLevelNumber)
    filePath = folderPath + "/" + fileList[index] + ".txt"
    print(fileList)
    
    running = True
    #  print(fileList)
    text = algo
    algo = "bfs"
    
    while running:
        # screen.fill(BG_COLOR)
        screen.blit(background, (0, 0))
        
        # get origin data 
        temp = fileList[index].replace("Level", "Input")
        inputFile = "../../Input/" + temp + ".txt"
        # print(inputFile)
        weightStone, board = readFile(inputFile)
        startPos, stonePos, switchPos = findPosition(board, weightStone)
        
        
        # get data
        result, algorithmList = readResult(filePath)
        # print(algorithmList)
        # print(result.)
        # print(algorithmList)
        path = result[algo].path
        weight = result[algo].weight
        # algo.upper()
        
        # get level and delete .txt
        fileList = sorted([f[:-4] for f in os.listdir(folderPath) if f.endswith(".txt")],key=extractLevelNumber)
        # draw name of level
        
        drawText(screen, fileList[index], 40)    
        # print(fileList[index])  
        
        # draw title
        drawTitle(screen)
        
        #draw board
        drawBoard(screen, board, width/2 - (len(board[0]) * 50 / 2 - 10), 235)
        
        # button
        buttonLeft, buttonRight = buttonChoice(screen)
        
        # draw button play
        buttonPlay = drawButtonPlay(screen, board)
       
        # text.upper()
        buttonAlgorithm = drawButtonAlgorithm(screen, text)
        
        
        
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttonRight.collidepoint(event.pos):
                    if 0 <= index < len(fileList) - 1:
                        index += 1
                        filePath = folderPath + "/" + fileList[index] + ".txt"
                if buttonLeft.collidepoint(event.pos):
                    if 0 < index < len(fileList) :
                        index -= 1
                        filePath = folderPath + "/" + fileList[index] + ".txt"
                if buttonPlay.collidepoint(event.pos):
                        screen.fill((255, 255, 255))
                        switchToMove(screen, board, startPos, stonePos, switchPos ,path, weight, index, algo) 
                           
                if buttonAlgorithm.collidepoint(event.pos):
                    algoButton, algo = drawListAlgorithm(screen, algorithmList)
                    text = algo
                    algo = algo.lower()
                    print("Choice: " + str(algo))
                    

        # print("index " + str(index))
        
        
def main():
    runHome(0, "Select the algorithm")
    
    
if __name__ == "__main__":
   main()