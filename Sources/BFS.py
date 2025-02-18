import supportFile as spf
import time
import tracemalloc


def output(filePath, newSate, time, memory):
    with open(filePath, "w") as f:
        f.write("BFS\n")
        f.write("Steps: " + str(newSate.steps) + " , Weight: " + str(newSate.weightPush) + " , Node: " + str(newSate.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
        f.write("Path: " + newSate.path + "\n")
    

def BFS(filePath, board, weightStone):
    startPos, stonePos, switchPos = spf.findPosition(board, weightStone)
    
    # use to debug weight
    # print("dai: " + str(len(board)) + " Rong: " + str(len(board[0])))
    # print("Position stone: " + str(stonePos))
    print(switchPos)
    
    # calculate time and memory
    startTime = time.time()
    tracemalloc.start()
    
    # set the first state
    startState = spf.state(board, None, "", 0, 0)
    listState = [startState]
    listVisited = [startState]
    node = 0
    weight = 0
    
    # starting BFS:
    while len(listVisited) != 0:
        nowState = listVisited.pop(0)
        curPos = spf.findPosAres(nowState.board)
        
        # direction of next step
        directions  = spf.nextDirections(nowState.board, curPos)
        
        for nextPos in directions:
            
            # get weight stone 
            weight = spf.checkWeight(nowState.board, stonePos, nextPos)
            
            # create the new board when move
            newBoard = spf.move(nowState.board, stonePos ,nextPos, curPos, switchPos)
            
            # update node visited
            node += 1
            
            # check conditions 
            if spf.checkSameBoard(newBoard, listState):
                continue
            
            # get the path:
            nameDirection = spf.moveDirection(nowState.board, nextPos, curPos)  
            
            newState = spf.state(newBoard, nowState.board, nowState.path + nameDirection, nowState.weightPush + weight, node)
            
            # use to debug
            spf.printBoard(newState.board)
            
            # end the function
            if spf.checkWinner(newBoard, switchPos):
                
                timeUsed = (time.time() - startTime) * 1000
                timeUsed = int(timeUsed)
                currentMemory, peakMemory = tracemalloc.get_traced_memory() 
                tracemalloc.stop()
                memoryUsed = round((peakMemory / (1024 * 1024)), 3)
                
                
                output(filePath, newState, timeUsed, memoryUsed)
                print("------------------------")
                print("Founded the path: ")
                print("Steps: " + str(newState.steps) + " , Weight: " + str(newState.weightPush) + " , Node: " + str(newState.node))
                print(newState.path )
                return newState
            
            listState.append(newState)
            listVisited.append(newState)
            
            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                return []
            
            
    print("Not found")
    return []