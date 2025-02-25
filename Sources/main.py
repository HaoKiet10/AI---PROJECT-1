import supportFile as spf
import BFS
import UCS
import DFS

import pygame
import tkinter as tk
import sys
# sys.path.append("../UI/Source/")
# import Move as mov
# import Home as ho


inputFileName = "../Input/Input-1.txt"
outputFileName = inputFileName.replace("Input", "Output")


def readFile(inputFile):
    with open(inputFile, 'r') as file: 
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
    weightStone, board = readFile(inputFileName)
    # bfsSate = BFS.BFS(outputFileName, board, weightStone)
    # root = tk.Tk()
    # app = Sokoban(root)
    # root.mainloop() 
    
    
    startPos, stonePos, switchPos = spf.findPosition(board, weightStone)
    path = "uRRRRU"
    # mov.run(board, startPos, stonePos, switchPos ,path)
    ho.runHome(board, startPos, stonePos, switchPos ,path)
    
    # dfs = DFS.DFS(outputFileName, board, weightStone)
    # ucs = UCS.UCS(board, weightStone, outputFileName)
    # dfs = DFS.DFS(outputFileName, board, weightStone)

if __name__ == "__main__":
    main()