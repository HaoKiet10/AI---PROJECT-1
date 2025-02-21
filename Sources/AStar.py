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

def AStar(board, weightStone, filePath):
	# initialize open (priority queue), closed (list) and tentative
	open = PriorityQueue()
	tentative : list[spf.state] = []
	closed : list[spf.state] = []

	# push the starting state into open
	curPos, stoneList, switchPos = spf.findPosition(board, weightStone)
	startState = spf.state(board, None, None, 0, 0, stoneList)
	open.put(startState)

	# while loop to implement A*
	# while not open.empty():
	# 	curState : spf.state = open.get()
	# 	curPos = spf.findPosAres(curState.board)
	# 	nextDir = spf.nextDirections(curState.board, curState.stonePos, curPos, curPos, )
	# 	for dir in nextDir:
	# 		# create new map state with the found directions
	# 		spf.move(curState.board, curState.stonePos, nextDir)
	# 		# check if current direction have existed inside closed. 
			

	




	