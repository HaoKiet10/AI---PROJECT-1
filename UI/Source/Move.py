import pygame
import time
from copy import deepcopy
from screenManager import switchToHome


# Parameter for screen
SIZE = 50
UI_WIDTH = 300
FRONT_SIZE = 36
BG_COLOR = (255, 255, 255)
width = 1000
height = 800



textures = {
    "*" : pygame.transform.scale(pygame.image.load("../Assets/goal.png"), (SIZE, SIZE)),
    "." : pygame.transform.scale(pygame.image.load("../Assets/switch_4.png"), (SIZE, SIZE)),
    "$" : pygame.transform.scale(pygame.image.load("../Assets/box_1.png"), (SIZE, SIZE)),
    "#" : pygame.transform.scale(pygame.image.load("../Assets/wall_3.png"), (SIZE, SIZE)),
    " " : pygame.transform.scale(pygame.image.load("../Assets/ground_1.png"), (SIZE, SIZE)),
    "@" : pygame.transform.scale(pygame.image.load("../Assets/player.png"), (SIZE, SIZE))
}

imageQuit = pygame.transform.scale(pygame.image.load("../Assets/quit_1.png"), (80, 90))
background = pygame.transform.scale(pygame.image.load("../Assets/background.png"), (width, height))

def drawBoard(screen, board, x, y):
    for i in range(len(board)):
        for j in range(len(board[0])):
            image = textures.get(" ", textures[" "])
            screen.blit(image, (x + j * SIZE, y + i * SIZE + 50))
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            tile = board[i][j]
            image = textures.get(tile, textures[" "])
            screen.blit(image, (x + j * SIZE, y + i * SIZE + 50))

def drawScore(screen, board,font, level, weight, steps):
    # parameter 1 and 2 are the x and y coordinates on the axis
    uiX = len(board[0]) * SIZE // 2 - 60
    uiY = len(board) * SIZE + 80
    # pygame.draw.rect(screen, (0, 0, 0), (uiX, uiY, len(board) * SIZE, len(board) * SIZE ))
    
    width, height = screen.get_size()
    text1 = [
        f"   Level:{level}" ,
        f"Weight:{weight}  " ,
        f"   Steps: {steps} " 
        # "",
       
    ]
    text2 = [
        "   [S]: Start",
        "[Space]: Pause",
        "    [R]: Reset"
    ]
    titile = "SOKOBAN"
    font1 = pygame.font.SysFont("comic sans ms", 50)
    label = font1.render(titile, True, (255, 255, 255))
    screen.blit(label, (width / 2 - 120, 10))

    font = pygame.font.SysFont("comic sans ms", 35)
    for i, text in enumerate(text1):
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (250 * i , height - 170))
    
    for i, text in enumerate(text2):
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (250 * i , height - 100))
    
    


# def updatedBoard()
def move(startPos, stonePos, dir):
    
    xAres, yAres = startPos
    oldStone, nextStone = (0, 0), (0, 0) 
    weightPush = 0
     # If Ares is pushing a stone
    if dir in 'UDLR':  
       
        dx, dy = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[dir]
        new_x, new_y = xAres + dx, yAres + dy
        oldStone = (new_x, new_y)
        # New stone position
        nextStone = (new_x + dx, new_y + dy)  
        if (oldStone[0], oldStone[1]) in stonePos:
            stonePos[(nextStone[0], nextStone[1])] = stonePos.pop((oldStone[0], oldStone[1]))
            weightPush = stonePos[(nextStone[0], nextStone[1])]
            print("Weight: " + str(weightPush))
        # If Ares is pushing a stone
        return (new_x, new_y), nextStone, oldStone, weightPush

    # Normal movement without pushing a stone
    elif dir in 'udlr':  
        dx, dy = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}[dir]
        new_x, new_y = xAres + dx, yAres + dy
        return (new_x, new_y), (0, 0), (0, 0), 0
    

    
    return startPos, (0, 0), (0, 0)  
    
            
def drawButtonReturn(screen, board):
    buttonReturn = pygame.Rect(width - 80, height - 100, 80, 90)
    # pygame.draw.rect(screen, (255, 255, 255), buttonReturn)
    screen.blit(imageQuit, (width - 80, height - 100))
    
    return buttonReturn
    

def run(screen, board, startPos, stonePos, switchPos,path, curLevel, algo):
    # pygame.init()
    # width = len(board[0]) * SIZE  + UI_WIDTH
    # height = len(board) * SIZE + 50
    

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban map")
    print("vi tri ban dau: " + str(startPos))
    
    font = pygame.font.Font(None, FRONT_SIZE)
    clock = pygame.time.Clock()
    
    # save to reset
    originPos = startPos
    originBoard = deepcopy(board)

    running = True
    check = True
    index = 0
    steps = 0
    level = curLevel + 1
    weight = 0
    paused = False
    
    
    
    
    while running:    

        
        # draw background
        screen.blit(background, (0, 0))
        
        
        drawScore(screen, board, font, level, weight, steps)
        drawBoard(screen, board, (width / 2 ) - (len(board[0]) * 50 / 2), 100)
        buttonReturn = drawButtonReturn(screen, board)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False 
                if event.key == pygame.K_r:
                    index = 0
                    steps = 0
                    paused = False
                    startPos = originPos
                    board = deepcopy(originBoard)
                    # drawScore(screen, board, font, level, weight, steps)
                    # drawBoard(screen, board)
                    # pygame.display.flip()
                    
                if event.key == pygame.K_s:
                    paused = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttonReturn.collidepoint(event.pos):
                    screen.fill((255, 255, 255))
                    switchToHome(curLevel, algo)
                    
                    
        
        
        if index < len(path) and paused:
            dir = path[index]
            print(dir)
            
            # if board[startPos[0]][startPos[1]] !=  '*':
            #     board[startPos[0]][startPos[1]] = '.'
             
            board[startPos[0]][startPos[1]] = ' '
            startPos, nextStone, oldStone, weightPush = move(startPos, stonePos, dir)
            # print("Position of stone: " + str(stonePos))
            weight += weightPush
            
            print("vi tri da cu " + str(oldStone))
            print("vi tri da moi " + str(nextStone))
            print("vi tri ares: " + str(startPos))
        
            
            if board[oldStone[0]][oldStone[1]] == '$':
                board[oldStone[0]][oldStone[1]] = ' '
                board[nextStone[0]][nextStone[1]] = '$'
            
            elif board[oldStone[0]][oldStone[1]] == '*':
                board[oldStone[0]][oldStone[1]] = '.'
                board[nextStone[0]][nextStone[1]] = '$' 
            
            board[startPos[0]][startPos[1]] = '@'
            
            for i in switchPos:
                if board[i[0]][i[1]] == '$':
                    board[i[0]][i[1]] = '*'
                elif board[i[0]][i[1]] != '*':
                    board[i[0]][i[1]] = '.'
                
          
            
            for i in range(len(board)):
                print(board[i])
            print("--------------------")
            
         
            
            index += 1
            steps += 1
            screen.blit(background, (0, 0))
             
            drawScore(screen, board, font, level, weight, steps)
            drawBoard(screen, board, (width / 2 ) - (len(board[0]) * 50 / 2), 100)
            buttonReturn = drawButtonReturn(screen, board)
            
            
            pygame.display.flip()
            # clock.tick(2)
            time.sleep(0.1)
        
               
    pygame.quit()
    
    
    
