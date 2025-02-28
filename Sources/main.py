import supportFile as spf
import BFS
import DFS
import UCS
import AStar
import Swarm



inputFileName = "../Input/Input-7.txt"
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
    print("BFS running")
    bfs = BFS.BFS(outputFileName, board, weightStone)
    print("DFS running")
    dfs = DFS.DFS(outputFileName, board, weightStone)
    print("UCS running")
    ucs = UCS.UCS(board, weightStone, outputFileName)
    print("A* running")
    aStar = AStar.AStar(board, weightStone, outputFileName)
    print("ACO running")
    aco = Swarm.ACO(outputFileName, board, weightStone)

    
if __name__ == "__main__":
    main()