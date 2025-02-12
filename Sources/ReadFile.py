with open("input.txt", 'r') as file: 
    line = file.readlines()

weightStone = list(map(int, line[0].strip().split()))

array = []
for line in line[1:]:
    if line.strip():
        array.append(line.rstrip())
        