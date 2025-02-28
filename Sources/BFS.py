import supportFile as spf
import time
import tracemalloc
import copy


def output(filePath, newState, time, memory):
    #  output 
    with open(filePath, "a") as f:
        if newState is None:
            f.write("Not found")
            return None
        f.write("BFS\n")
        f.write("Steps: " + str(newState.steps) + " , Weight: " + str(newState.weightPush) + " , Node: " + str(newState.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
        f.write("Path: " + newState.path + "\n")
    
    newName = "-" + filePath.split("-")[-1]
    filePathData = "../UI/Data/Level" + newName
    
    with open(filePathData, "w") as f:
        f.write("BFS \n")
        f.write(newState.path + "\n")
        f.write(str(newState.weightPush) + "\n")
    
def ending(startTime, filePath, cur_map):
    timeUsed = (time.time() - startTime) * 1000
    timeUsed = int(timeUsed)
    currentMemory, peakMemory = tracemalloc.get_traced_memory() 
    tracemalloc.stop()
    memoryUsed = round((peakMemory / (1024 * 1024)), 3)
    output(filePath, cur_map, timeUsed, memoryUsed)
    return cur_map


def BFS(filePath, board, weightStone):
    startPos, stonePos, switchPos = spf.findPosition(board, weightStone)
    
    # use to debug weight
    # print("dai: " + str(len(board)) + " Rong: " + str(len(board[0])))
    # print("Position stone: " + str(stonePos))
    # print(stonePos)
    # print(switchPos)
    
    # calculate time and memory
    startTime = time.time()
    tracemalloc.start()
    
    # set the first state
    
    startState = spf.state(board, None, "", 0, 0, stonePos)
    listState = [startState]
    listVisited : set[spf.state]= set()
    node = 0
    weight = 0
    
    # starting BFS:
    while len(listState) != 0:
        nowState = listState.pop(0)
        curPos = spf.findPosAres(nowState.board)
        node += 1
        
        # direction of next step
        directions  = spf.nextDirections(nowState.board, curPos)
        
        for nextPos in directions:
            
            # get weight stone 
            weight = spf.checkWeight(nowState.board, nowState.stonePos, nextPos)
        
            # create the new board when move
    
            newBoard, newStonePos = spf.move(nowState.board, nowState.stonePos, nextPos, curPos, switchPos)
            # get the path:
            nameDirection = spf.moveDirection(nowState.board, nextPos, curPos)  
            
            newState = spf.state(newBoard, nowState, nowState.path + nameDirection, nowState.weightPush + weight, node, newStonePos)
            if newState in listVisited:
                continue
            """use to debug
            spf.printBoard(newState.board, newState.stonePos)"""
            
            # end the function
            if spf.checkWinner(nowState.board, switchPos):
                return ending(startTime, filePath, nowState)            
            listState.append(newState)
            listVisited.add(nowState)
            
            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                # print("Not enought time")
                return ending(startTime, filePath, nowState)
            
            
    # print("Not found")
    return ending(startTime, filePath, nowState)