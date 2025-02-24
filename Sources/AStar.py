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

# function to check if a state is already reached and saved inside an
# array or not. If yes return the index, if not return -1.
def checkExist(newBoard, newStonePos, arr : list[spf.state]):
	count = 0
	# print("Length arr: ", len(arr))
	for state in arr:
		if newBoard == state.board and newStonePos == state.stonePos:
			return count
		# print(count)
		count += 1	
	return -1	

# function to output results to an specified output file. Values include number of steps, weight pushed, number of nodes (states) visited, time, memory cost and the shortest path. 
def output(finalState: spf.state, time, memory, filePath):
	tracePath(finalState)
	with open(filePath, "a") as file:
		file.write("A-Star\n")
		file.write("Steps: " + str(finalState.steps) + ", Weight: " + str(finalState.weightPush) + ", Node: " + str(finalState.node) + ", Time (ms): " + str(time) + ", Memory (MB): " + str(memory) + "\n")
		file.write("Path: " + finalState.path + "\n")

# function for traceback the path from the initial state to goal state
def tracePath(curState : spf.state):
	if curState.preState == None:
		return
	tracePath(curState.preState)
	pprint(curState.board)
	print(curState.stonePos)
	print(curState.weightPush)

def AStar(board, weightStone, filePath):
	# time and memory trackers
	startTime = time.time()
	tracemalloc.start()

	# initialize open (priority queue), closed (list) and tentative
	open = PriorityQueue()
	tentative : list[spf.state] = []
	closed : list[spf.state] = []

	# push the starting state into open
	curPos, stonePos, switchPos = spf.findPosition(board, weightStone)
	startState = spf.state(board, None, "", 0, 0, stonePos)
	open.put(startState)

	# while loop to implement A*
	while not open.empty():
		curState : spf.state = open.get()
		curPos = spf.findPosAres(curState.board)

		if checkExist(curState.board, curState.stonePos, closed) != -1:
			continue
		closed.append(curState)

		# check if current state is goal state
		if spf.checkWinner(curState.board, switchPos):
			elapsedTime = (time.time() - startTime) * 1000

			curMemory, peakMemory = tracemalloc.get_traced_memory()
			peakMemory = peakMemory / (1024 * 1024)
			tracemalloc.stop()

			output(curState, elapsedTime, peakMemory, filePath)
			return curState

		# find possible moves
		nextDir = spf.nextDirections(curState.board, curPos)

		for dir in nextDir:
			# create new map state with the found directions
			newBoard, newStonePos = spf.move(curState.board, curState.stonePos, dir, curPos, switchPos)

			# check if the new state have existed inside closed. 
			if checkExist(newBoard, newStonePos, closed) != -1:
				continue

			# check if current path to new direction have lower cost than
			# already known paths in tentative.
			index = checkExist(newBoard, newStonePos, tentative)

			# Calculate the new total cost and the new amount of weight pushed separately.
			newCost = 1 + spf.checkWeight(curState.board, curState.stonePos, dir)
			newWeightPushed = curState.weightPush + newCost - 1
			newTotalCost = curState.weightPush + curState.steps + newCost

			newPath = curState.path + spf.moveDirection(curState.board, dir, curPos)
			newState = spf.state(newBoard, curState, newPath, newWeightPushed, curState.node, newStonePos)
			# case if this state is completely new
			if index == -1:
				newState.node += 1
				tentative.append(newState)
				open.put(newState)
			# case if this state existed in tentative but can be improved
			elif tentative[index].steps + tentative[index].weightPush > newTotalCost:
				tentative[index] = newState
				open.put(newState)

	

				
			

	




	