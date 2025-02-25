import pygame
import time
from copy import deepcopy
from screenManager import switchToHome


# Parameter for screen
SIZE = 50
UI_WIDTH = 300
FRONT_SIZE = 36
BG_COLOR = (255, 255, 255)



textures = {
    "*" : pygame.transform.scale(pygame.image.load("../Assets/goal.png"), (SIZE, SIZE)),
    "." : pygame.transform.scale(pygame.image.load("../Assets/switch.png"), (SIZE, SIZE)),
    "$" : pygame.transform.scale(pygame.image.load("../Assets/box.png"), (SIZE, SIZE)),
    "#" : pygame.transform.scale(pygame.image.load("../Assets/wall.png"), (SIZE, SIZE)),
    " " : pygame.transform.scale(pygame.image.load("../Assets/free_1.png"), (SIZE, SIZE)),
    "@" : pygame.transform.scale(pygame.image.load("../Assets/figure.png"), (SIZE, SIZE))
}

imageQuit = pygame.transform.scale(pygame.image.load("../Assets/quit.png"), (SIZE, SIZE))

def drawBoard(screen, board, x, y):
    for i in range(len(board)):
        for j in range(len(board[0])):
            tile = board[i][j]
            image = textures.get(tile, textures[" "])
            screen.blit(image, (x + j * SIZE, y + i * SIZE + 50))

def drawScore(screen, board,font, level, weight, steps):
    # parameter 1 and 2 are the x and y coordinates on the axis
    uiX = len(board[0]) * SIZE 
    pygame.draw.rect(screen, (0, 0, 0), (uiX, 50, UI_WIDTH, len(board) * SIZE))
    
    width, height = screen.get_size()
    texts = [
        f"Level: {level}" ,
        f"Weight: {weight}" ,
        f"Steps: {steps}" 
        "",
        "[S] Start",
        "[ ] Pause",
        "[R] Reset"
    ]
    titile = "SOKOBAN"
    label = font.render(titile, True, (255, 255, 255))
    screen.blit(label, (width / 2 - 70, 10))

    
    for i, text in enumerate(texts):
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (uiX + 50 ,70 + i * 40))
    


# def updatedBoard()
def move(startPos, dir):
    
    xAres, yAres = startPos
    oldStone, nextStone = (0, 0), (0, 0) 

     # If Ares is pushing a stone
    if dir in 'UDLR':  
       
        dx, dy = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[dir]
        new_x, new_y = xAres + dx, yAres + dy
        oldStone = (new_x, new_y)
        # New stone position
        nextStone = (new_x + dx, new_y + dy)  

        # If Ares is pushing a stone
        return (new_x, new_y), nextStone, oldStone

    # Normal movement without pushing a stone
    elif dir in 'udlr':  
        dx, dy = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}[dir]
        new_x, new_y = xAres + dx, yAres + dy
        return (new_x, new_y), (0, 0), (0, 0)  
    

    
    return startPos, (0, 0), (0, 0)  
    
            
def drawButtonReturn(screen, board):
    uiX = len(board[0]) * SIZE 
    buttonReturn = pygame.Rect(uiX + 60, 370, 50, 60)
    pygame.draw.rect(screen, (255, 255, 255), buttonReturn)
    screen.blit(imageQuit, (uiX + 60, 370))
    
    return buttonReturn
    

def run(screen, board, startPos, stonePos, switchPos,path, weightPush, curLevel, algo):
    # pygame.init()
    # width = len(board[0]) * SIZE  + UI_WIDTH
    # height = len(board) * SIZE + 50
    
    width = 1000
    height = 700
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
    weight = weightPush
    paused = False
    
    
    
    
    
    while running:    
        screen.fill(BG_COLOR)
        
        
        drawScore(screen, board, font, level, weight, steps)
        drawBoard(screen, board, 0, 0)
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
            board[startPos[0]][startPos[1]] = ' '
            startPos, nextStone, oldStone = move(startPos, dir)
            screen.fill(BG_COLOR) # background Color
            
            print("vi tri da cu " + str(oldStone))
            print("vi tri da moi " + str(nextStone))
            print("vi tri ares: " + str(startPos))
            if board[oldStone[0]][oldStone[1]] == '$':
                board[oldStone[0]][oldStone[1]] = ' '
                board[nextStone[0]][nextStone[1]] = '$'
            
            board[startPos[0]][startPos[1]] = '@'
            
            for i in switchPos:
                if board[i[0]][i[1]] == '$':
                    board[i[0]][i[1]] = '*'
            
                
          
            
            for i in range(len(board)):
                print(board[i])
            print("--------------------")
            
         
            
            index += 1
            steps += 1
            
            drawBoard(screen, board, 0, 0)
            drawScore(screen, board, font, level, weight, steps)
            buttonReturn = drawButtonReturn(screen, board)
            
            pygame.display.flip()
            # clock.tick(2)
            time.sleep(0.5)
        
               
    pygame.quit()
    
    
    
