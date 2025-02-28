from pprint import pprint
from queue import PriorityQueue
import time
import tracemalloc
import supportFile as spf

def output(filePath, cur_map, time, memory):
    with open(filePath, "a") as f:
        f.write("UCS\n")
        if cur_map == None:
            f.write("Notfound")
            return
        else:
            # traceback(cur_map)  
            f.write("Steps: " + str(cur_map.steps) + " , Weight: " + str(cur_map.weightPush) + " , Node: " + str(cur_map.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
            f.write("Path: " + cur_map.path + "\n")
            
    newName = "-" + filePath.split("-")[-1]
    filePathData = "../UI/Data/Level" + newName
    
    with open(filePathData, "a") as f:
        f.write("UCS \n")
        f.write(cur_map.path + "\n")
        f.write(str(cur_map.weightPush) + "\n")
    

def ending(startTime, filePath, cur_map):
    timeUsed = (time.time() - startTime) * 1000
    timeUsed = int(timeUsed)
    currentMemory, peakMemory = tracemalloc.get_traced_memory() 
    tracemalloc.stop()
    memoryUsed = round((peakMemory / (1024 * 1024)), 3)
    output(filePath, cur_map, timeUsed, memoryUsed)
    return cur_map

def traceback(cur_map):
    if cur_map.preState == None:
        return
    traceback(cur_map.preState)
    pprint(cur_map.board)
    print(cur_map.stonePos) 
    print(cur_map.weightPush)


def UCS(board, weightedStone, filePath):
    startTime = time.time()
    tracemalloc.start()
    Ares, stoneList, switchList = spf.findPosition(board, weightedStone)

    start_map = spf.state(board, None, "", 0, 0, stoneList)
    if spf.checkWinner(board, switchList):
        return board


    visited_map : set[spf.state] = set()
    list_map = PriorityQueue()
    list_map.put((start_map.weightPush + start_map.steps, start_map))
    node = 0

    # j = 410
    # while j > 0:
    while not list_map.empty():
        node += 1
        priority, cur_map = list_map.get()
        cur_map.node = node
        visited_map.add(cur_map)
        Ares = spf.findPosAres(cur_map.board)

        if spf.checkWinner(cur_map.board, switchList):
            return ending(startTime, filePath, cur_map)

        next_direction = spf.nextDirections(cur_map.board, Ares)
        for i in next_direction:
            new_board, newStonePos = spf.move(cur_map.board, cur_map.stonePos, i, Ares, switchList)
            path = cur_map.path + spf.moveDirection(cur_map.board, i, Ares)
            weight = cur_map.weightPush + spf.checkWeight(cur_map.board, cur_map.stonePos, i)
            new_map = spf.state(new_board, cur_map, path, weight, node, newStonePos)

            if new_map in visited_map:
                continue
            list_map.put((new_map.weightPush + new_map.steps, new_map))

            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                return ending(startTime, filePath, None)
               
        # j-=1
    
    return ending(startTime, filePath, None)
