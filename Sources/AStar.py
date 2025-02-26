# – “#” for walls.
# – “ ” (whitespace) for free spaces.
# – “$” for stones.
# – “@” for Ares.
# – “.” for switch places.
# – “*” for stones placed on switches.
# – “+” for Ares on a switch.

from queue import PriorityQueue
import supportFile as spf
import time
import tracemalloc
from pprint import pprint

# function to output results to an specified output file. Values include number of steps, weight pushed, number of nodes (states) visited, time, memory cost and the shortest path. 
def output(finalState: spf.state, time, memory, filePath):
	tracePath(finalState)
	with open(filePath, "a") as file:
		file.write("A-Star\n")
		file.write("Steps: " + str(finalState.steps) + ", Weight: " + str(finalState.weightPush) + ", Node: " + str(finalState.node) + ", Time (ms): " + str(time) + ", Memory (MB): " + str(memory) + "\n")
		file.write("Path: " + finalState.path + "\n")
  
	newName = "-" + filePath.split("-")[-1]
	filePathData = "../UI/Data/Level" + newName

	with open(filePathData, "a") as f:
		f.write("Astar \n")
		f.write(finalState.path + "\n")
		f.write(str(finalState.weightPush) + "\n")
        
   
# function for traceback the path from the initial state to goal state
def tracePath(curState : spf.state):
	if curState.preState == None:
		return
	tracePath(curState.preState)
	pprint(curState.board)
	print(curState.stonePos)
	print(curState.weightPush)

def ManhattanDist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def buildDistTable(stonePos, switchPos):
	costMatrix : list[list[int]] = []
	switchPos_list = list(switchPos)
	for x, y in stonePos.items():
		curList = []
		for s in switchPos_list:
			estiDist = ManhattanDist(x, s)
			curList.append(estiDist * y)
		costMatrix.append(curList)
	return costMatrix


def AStar(board, weightStone, filePath):
	# time, memory and node visited trackers
	startTime = time.time()
	tracemalloc.start()
	node = 1

	# initialize open (priority queue), closed (list) and tentative
	open = PriorityQueue()
	closed : set[spf.state] = set()

	# push the starting state into open
	curPos, stonePos, switchPos = spf.findPosition(board, weightStone)
	startState = spf.state(board, None, "", 0, node, stonePos)
	open.put(startState)

	# while loop to implement A*
	while not open.empty():
		curState : spf.state = open.get()
		curPos = spf.findPosAres(curState.board)
		node += 1

		if curState in closed:
			continue
		closed.add(curState)

		# check if current state is goal state
		if spf.checkWinner(curState.board, switchPos):
			elapsedTime = int((time.time() - startTime) * 1000)

			curMemory, peakMemory = tracemalloc.get_traced_memory()
			peakMemory = round(peakMemory / (1024 * 1024), 3)
			tracemalloc.stop()

			output(curState, elapsedTime, peakMemory, filePath)
			return curState

		# find possible moves
		nextDir = spf.nextDirections(curState.board, curPos)

		for dir in nextDir:
			# create new map state with the found directions
			newBoard, newStonePos = spf.move(curState.board, curState.stonePos, dir, curPos, switchPos)

			# Calculate the new total cost and the new amount of weight pushed separately.
			newCost = 1 + spf.checkWeight(curState.board, curState.stonePos, dir)
			newWeightPushed = curState.weightPush + newCost - 1

			newPath = curState.path + spf.moveDirection(curState.board, dir, curPos)
			newState = spf.state(newBoard, curState, newPath, newWeightPushed, node, newStonePos)

			# check if the new state have existed inside closed. 
			if newState in closed:
				continue
			else:
				open.put(newState)
	print("Not found") 
	return None

	

				
			

	




	