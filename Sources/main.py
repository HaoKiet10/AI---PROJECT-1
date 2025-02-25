import supportFile as spf
import BFS
import DFS
import UCS
import AStar

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
    weightStone, array = readFile()
    # bfsState = BFS.BFS(outputFileName, array, weightStone)
    ucs = UCS.UCS(array, weightStone, outputFileName)
    # dfs = DFS.DFS(outputFileName, array, weightStone)
    aStar = AStar.AStar(array, weightStone, outputFileName)
    
if __name__ == "__main__":
    main()