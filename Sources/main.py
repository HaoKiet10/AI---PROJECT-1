import supportFile as spf
import BFS
import DFS
import UCS
<<<<<<< Updated upstream

=======
import DFS
import Swarm

# import pygame
# import tkinter as tk
# import sys
# sys.path.append("../UI/Source/")
# import home as ui


>>>>>>> Stashed changes
inputFileName = "Input/Input-01.txt"
outputFileName = inputFileName.replace("Input", "Output")

def readFile():
    with open(inputFileName, 'r') as file: 
        line = file.readlines()

    weightStone = list(map(int, line[0].strip().split()))  # get value and assign to list

    array_1D = []
    for line in line[1:]:
        if line.strip():
            array_1D.append(line.rstrip())

    array = [list(ch) for ch in array_1D] # convert 1D to 2D
    
    with open(outputFileName, "w") as file:
        pass
    
    return weightStone, array



def main():
<<<<<<< Updated upstream
    weightStone, array = readFile()
    # bfsState = BFS.BFS(outputFileName, array, weightStone)
    ucs = UCS.UCS(array, weightStone, outputFileName)
    # dfs = DFS.DFS(outputFileName, array, weightStone)
    
=======
    weightStone, board = readFile()
    # bfsState = BFS.BFS(outputFileName, board, weightStone)
    # ucs = UCS.UCS(board, weightStone, outputFileName)
    # root = tk.Tk()
    # app = Sokoban(root)
    # root.mainloop() 
    # ui.run(board)
    # dfs = DFS.DFS(outputFileName, board, weightStone)
    # ucs = UCS.UCS(board, weightStone, outputFileName)
    # dfs = DFS.DFS(outputFileName, board, weightStone)
    swarm = Swarm.ACO(outputFileName, board, weightStone)
>>>>>>> Stashed changes
if __name__ == "__main__":
    main()