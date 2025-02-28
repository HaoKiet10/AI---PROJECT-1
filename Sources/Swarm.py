
"CAUTION EASY MAP USAGE ONLY"
"USE FOR OPTIMIZATION"



from pprint import pprint
from queue import PriorityQueue
import time
import tracemalloc
import supportFile as spf
import numpy as np
import random


"ANT COLONY OPTIMIZATION ALGORITHM PARAMETER"
"1 stone set ANT POPULATION to 20, 2 stone set to 100"
"Increase MAX_ITERATION for more optimize path"
MAX_ITERATION = 100
ANT_POPULATION = 100
EVAPORATION_RATE = 0.5
PHEROMONES_BOOST = 10
ALPHA = 1.0
BETA = 2.0

NODE_EXPAND = 0

def output(filePath, cur_map, time, memory):
    with open(filePath, "a") as f:
        f.write("Swarm\n")
        if cur_map == None:
            f.write("Notfound")
        else:
            traceback(cur_map)  
            f.write("Steps: " + str(cur_map.steps) + " , Weight: " + str(cur_map.weightPush) + " , Node: " + str(cur_map.node) + " , Time (ms): " + str(time) + " , Memory (MB): " + str(memory) + "\n")
            f.write("Path: " + cur_map.path + "\n")

    newName = "-" + filePath.split("-")[-1]
    filePathData = "../UI/Data/Level" + newName
    
    with open(filePathData, "a") as f:
        f.write("ACO \n")
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

def calculateHeuristic(stoneList, switchList):
    heuristic_value = 0
    stoneCoordinate = list(stoneList.keys())
    switchCoordinate = list(switchList)
    for i in range(len(stoneList)):
        heuristic_value += 1 / (1 + np.linalg.norm(np.array(stoneCoordinate[i]) - np.array(switchCoordinate[i]), ord = 1))
    return heuristic_value

def updatePheromones(paths, pheromones):
    pheromones *= EVAPORATION_RATE

    for path in paths:
        if path[-1] == (-1, -1):
            reward = PHEROMONES_BOOST / (len(path) - 1)
            for position in path:
                pheromones[position] += reward

def ACO(filePath, board, weightStone):
    startTime = time.time()
    tracemalloc.start()
    ares, stoneList, switchList = spf.findPosition(board, weightStone)
    startState = spf.state(board, None, "", 0, NODE_EXPAND, stoneList)
    pheromones = np.ones((len(board), len(board[0])))

    succesState = PriorityQueue()
    for iteration in range(MAX_ITERATION):
        print("Iteration:", iteration)
        paths = []
        for orderOfAnt in range(ANT_POPULATION):
            # print("Ant:", orderOfAnt, "moving")
            path, state = moveAnt(startState, switchList, pheromones)
            paths.append(path)
            if state is not None:
                succesState.put(state)
            endTime = time.time()
            if endTime - startTime > spf.TIMEOUT:
                return ending(startTime, filePath, None)
    print("End iteration")
    if not succesState.empty():
        optimized_path = succesState.get()
    else:
        optimized_path = None
    ending(startTime, filePath, optimized_path)
    return optimized_path

    

def moveAnt(startState, switchList, pheromones):
    global NODE_EXPAND
    NODE_EXPAND -= 1
    cur_state = startState
    cur_pos = spf.findPosAres(cur_state.board)
    path = [cur_pos]
    visitedState : set[spf.state] = set()
    while not spf.checkWinner(cur_state.board, switchList):
        NODE_EXPAND += 1
        probabilities = []
        available_move = []

        posible_move = spf.nextDirections(cur_state.board, cur_pos)
        for move in posible_move:
            newBoard, newStoneList = spf.move(cur_state.board, cur_state.stonePos, move, cur_pos, switchList)
            newWeightPush = spf.checkWeight(cur_state.board, cur_state.stonePos, move) + cur_state.weightPush
            newPath = cur_state.path + spf.moveDirection(cur_state.board, move, cur_pos)
            newState = spf.state(newBoard, cur_state, newPath, newWeightPush, NODE_EXPAND, newStoneList)

            if newState in visitedState:
                continue
            tau = pheromones[move] ** ALPHA
            eta = calculateHeuristic(newStoneList, switchList) ** BETA
            probability = tau * eta

            available_move.append(newState)
            probabilities.append(probability)


        if not available_move:
            return path, None  # No valid moves left, ant stops

        probabilities = np.array(probabilities) / sum(probabilities)

        # Choose next move based on probability
        visitedState.add(cur_state)
        cur_state = random.choices(available_move, weights=probabilities)[0]
        cur_pos = spf.findPosAres(cur_state.board)
        path.append(cur_pos)
        available_move.clear()

    """FIND THE SOLUTION"""
    print("Found solution")
    path.append((-1, -1)) 
    return path, cur_state