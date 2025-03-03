import supportFile as spf
import time
import tracemalloc

def output(filePath, newState, time, memory):
    with open(filePath, "a") as f:
        if newState is None:
            f.write("Not found")
            return None
        f.write("DFS\n")
        f.write("Steps: " + str(newState.steps) + " , Weight: " + str(newState.weightPush) + " , Node: " + str(newState.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
        f.write("Path: " + newState.path + "\n")

    newName = "-" + filePath.split("-")[-1]
    filePathData = "../UI/Data/Level" + newName
    
    with open(filePathData, "a") as f:
        f.write("DFS \n")
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

def DFS(filePath, board, weightStone):
    startPos, stonePos, switchPos = spf.findPosition(board, weightStone)
    
    # use to debug weight
    # print("dai: " + str(len(board)) + " Rong: " + str(len(board[0])))
    # print("Position stone: " + str(stonePos))
    # print(switchPos)
    
    # calculate time and memory
    startTime = time.time()
    tracemalloc.start()
    
    # set these first state
    startState = spf.state(board, None, "", 0, 0, stonePos)
    stack = [startState]
    listState : set[startState] = set()
    node = 0
    weight = 0
    
    # starting DFS:
    while len(stack) != 0:
        nowState = stack.pop()
        curPos = spf.findPosAres(nowState.board)
        
        # direction of next step
        directions  = spf.nextDirections(nowState.board, curPos)
        
        for nextPos in directions:
            
            # get weight stone 
            weight = spf.checkWeight(nowState.board, nowState.stonePos, nextPos)
            
            # create the new board when move
            newBoard, newStonePos = spf.move(nowState.board, nowState.stonePos ,nextPos, curPos, switchPos)
            
            
            # update node visited
            node += 1
            
            # get the path:
            nameDirection = spf.moveDirection(nowState.board, nextPos, curPos)  
            
            newState = spf.state(newBoard, nowState.board, nowState.path + nameDirection, nowState.weightPush + weight, node, newStonePos)
            
            if newState in listState:
                continue
            # use to debug
            # spf.printBoard(newState.board)
            
            # end the function
            if spf.checkWinner(newBoard, switchPos):
                return ending(startTime, filePath, newState)
                
            
            listState.add(newState)
            stack.append(newState)
            
            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                return ending(startTime, filePath, None)
            
    # print("Not found")
    return ending(startTime, filePath, None)
