# – “#” for walls.
# – “ ” (whitespace) for free spaces.
# – “$” for stones.
# – “@” for Ares.
# – “.” for switch places.
# – “*” for stones placed on switches.
# – “+” for Ares on a switch.




from queue import PriorityQueue
import time
import tracemalloc
import supportFile as spf


def output(filePath, cur_map, time, memory):
    with open(filePath, "a") as f:
        f.write("UCS\n")
        f.write("Steps: " + str(cur_map.steps) + " , Weight: " + str(cur_map.weightPush) + " , Node: " + str(cur_map.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
        f.write("Path: " + cur_map.path + "\n")


def UCS(board, weightedStone, filePath):
    startTime = time.time()
    tracemalloc.start()
    Ares, stoneList, switchList = spf.findPosition(board, weightedStone)

    start_map = spf.state(board, None, "", 0, 0)
    if spf.checkWinner(board, switchList):
        return board


    visited_map = []
    list_map = PriorityQueue()
    list_map.put(start_map)
    node = 0

    while not list_map.empty():

        node += 1
        cur_map: spf.state = list_map.get()
        cur_map.node = node
        visited_map.append(cur_map)

        if spf.checkWinner(cur_map.board, switchList):
            timeUsed = (time.time() - startTime) * 1000
            timeUsed = int(timeUsed)
            currentMemory, peakMemory = tracemalloc.get_traced_memory() 
            tracemalloc.stop()
            memoryUsed = round((peakMemory / (1024 * 1024)), 3)
            output(filePath, cur_map, timeUsed, memoryUsed)
            return cur_map


        next_dỉrection = spf.nextDirections(cur_map.board, spf.findPosAres(cur_map.board))
        for i in next_dỉrection:
            new_board = spf.move(cur_map.board, stoneList, i, spf.findPosAres(cur_map.board), switchList)
            if not spf.checkSameBoard(new_board, visited_map):
                path = cur_map.path + spf.moveDirection(cur_map.board, i, spf.findPosAres(cur_map.board))
                weight = cur_map.weightPush + spf.checkWeight(cur_map.board, stoneList, i)
                new_map = spf.state(new_board, cur_map, path, weight, node)
                list_map.put(new_map)

            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                return None

    
    return None
