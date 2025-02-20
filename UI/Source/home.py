import pygame
import tkinter as tk 
from tkinter import filedialog, messagebox
import time

SIZE = 50

textures = {
    "*" : pygame.transform.scale(pygame.image.load("../UI/goal.png"), (SIZE, SIZE)),
    "." : pygame.transform.scale(pygame.image.load("../UI/switchs.png"), (SIZE, SIZE)),
    "$" : pygame.transform.scale(pygame.image.load("../UI/box.png"), (SIZE, SIZE)),
    "#" : pygame.transform.scale(pygame.image.load("../UI/wall.png"), (SIZE, SIZE)),
    " " : pygame.transform.scale(pygame.image.load("../UI/free_1.png"), (SIZE, SIZE)),
    "@" : pygame.transform.scale(pygame.image.load("../UI/figure.png"), (SIZE, SIZE))
}

def drawBoard(screen, board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            tile = board[i][j]
            image = textures.get(tile, textures[" "])
            screen.blit(image, (j * SIZE, i * SIZE))


def run(board):
    pygame.init()
    width = len(board[0]) * SIZE
    height = len(board) * SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban map")
    
    
    running = True
    while running: 
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                    running = False
         
        screen.fill((255, 255, 255))
        drawBoard(screen, board)
        pygame.display.flip()
                   
    pygame.quit()
    
    
    
class Sokoban:
    def __init__(self, root):
        self.root = root
        self.root.tile("Sokoban - Adventure of Ares")
        self.root.geometry("800x600") # size of window
        
        #Home
        self.mainFrame = tk.Fame(self.root)
        
        # allow the program expand ver and horzi
        self.mainFrame.pack(fill = "both", expand = True) 
        
        tk.Label(self.mainFrame, text = "Sokoban  - Ares Adventure", front = ("Arial", 20)).pack(pady = 10)
        
        # chocie algorithm 
        self.algorithmChoice = tk.StringVar()
        # set default value
        self.algorithmChoice.set("BFS") 
         
        tk.Label(self.mainFrame, text = "Choice Algorithm: ").pack()
        self.algorithmMenu = tk.OptionMenu(self.mainFrame, self.algorithmChoice, "BFS", "DFS", "A*", "UCS").pack(pady = 5)
          
        
        # Choice Map
        self.mapChoice = tk.StringVar()
        tk.Button(self.mainFrame, text = "Chocie map", command= self.loadMap).pack(pady = 5)
        self.mapLabel = tk.Label(self.mainFrame, text = "No selected").pack(pady = 5)
        
        tk.Button(self.mainFrame, text = "Play game", command=  self.root.quit()).pack(pady = 10)
        
        tk.Button(self.mainFrame, text = "Information about my Group", command =  self.root.quit()).pack(pady = 10)
        
        tk.Button(self.mainFrame, text = "Quit game", commad = self.root.quit()).pack(pady = 10)
        
        
    # def loadMap(self):
    #     fileName = filedialog.askopenfilename(title = "Chocie file map", filetypes = [("Text files", "*.txt")])
        
    #     if fileName:
    #         self.mapChoice.set(fileName)
            
    #         # get the final name when split
    #         self.mapLabel.config(text = f"Map: {fileName.split ('/')[-1]}") 
            
    # def startGame(self):
    #     if not self.mapChoice.get():
    #         messagebox.showwaring("Error", "Chocie the map")
           
         
    #     self.root.destroy() 
    #     playSokoban(self.mapChoice.get(), self.algorithmChoice.get())
        
        
    # def showInfo(self):
    #     messagebox.showinfor("Informatio of Group")



# root = tk.tk()
# app = Sokoban(root)
# root.mainloop()
        
            
            
            
        
        
        
        
        
        