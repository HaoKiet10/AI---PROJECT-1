import DFS


inputFileName = "../Input/Input-01.txt"
outputFileName = inputFileName.replace("Input", "Output")

''' Function to read input files'''
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
    ''' Create two lists storing stones's weigth and the map (array) ''' 
    weightStone, array = readFile()
    
    print(weightStone)
    print(array)
    
    
if __name__ == "__main__":
    main()