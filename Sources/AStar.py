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
import networkx

# function to output results to an specified output file. Values include number of steps, weight pushed, number of nodes (states) visited, time, memory cost and the shortest path. 
def output(finalState: spf.AStar_state, time, memory, filePath):
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
def tracePath(curState : spf.AStar_state):
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
	for x, y in stonePos.items():
		curList = []
		for s in switchPos:
			estiDist = ManhattanDist(x, s)
			curList.append(estiDist * y)
		costMatrix.append(curList)
	return costMatrix

def heuristicCalc(stonePos, switchPos):
	"""Our map consists of rocks and switches, of which we need to match one rock with one switch each. This correspond to a matching problem between two half of a bipartite graph, so we can visualize this as a minimum cost flow problem and solve it by such. Here I use python networkx module for simplicity."""
	# convert switchPos to an ordered list to build the cost matrix.
	switchPos_list = list(switchPos)
	costMatrix = buildDistTable(stonePos, switchPos)

	# create a directed graph
	G = networkx.DiGraph()
	
	# Add source node and sink node
	G.add_node('source', demand = -len(switchPos))
	G.add_node('sink', demand = len(switchPos))

	# Add edges between source and rocks
	for i, stone in enumerate(stonePos):
		G.add_edge("source", f"stone_{i}", capacity = 1, weight = 0)

	# Add nodes and edges from switches to sink
	for j, switch in enumerate(switchPos):
		G.add_edge(f"switch_{j}", "sink", capacity = 1, weight = 0) 
	
	# Add edges between stones and switches with costs
	for i, stone in enumerate(stonePos):
		for j, switch in enumerate(switchPos):
			cost = costMatrix[i][j]  # The cost of matching stone i to switch j
			G.add_edge(f"stone_{i}", f"switch_{j}", capacity=1, weight=cost)

	# Compute the min-cost max-flow
	cost, flow_dict = networkx.network_simplex(G)
	
	return cost
	
def AStar(board, weightStone, filePath):
	# time, memory and node visited trackers
	startTime = time.time()
	tracemalloc.start()
	node = 1

	# initialize open (priority queue), closed (list)  and tentative
	open = PriorityQueue()
	closed : set[spf.AStar_state] = set()

	# push the starting state into open
	curPos, stonePos, switchPos = spf.findPosition(board, weightStone)
	h = heuristicCalc(stonePos, switchPos)
	startState = spf.AStar_state(board, None, "", 0, node, stonePos, h)
	open.put(startState)

	# while loop to implement A*
	while not open.empty():
		curState : spf.AStar_state = open.get()
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

			# Calculate the new weightPushed and heuristic to add to the new node.
			newCost = spf.checkWeight(curState.board, curState.stonePos, dir)
			# Heuristic
			hCost = heuristicCalc(stonePos, switchPos)
			newWeightPushed = curState.weightPush + newCost
		
			newPath = curState.path + spf.moveDirection(curState.board, dir, curPos)
			newState = spf.AStar_state(newBoard, curState, newPath, newWeightPushed, node, newStonePos, hCost)

			# check if the new state have existed inside closed. 
			if newState in closed:
				continue
			else:
				open.put(newState)
	print("Not found") 
	return None

	

				
			

	




	