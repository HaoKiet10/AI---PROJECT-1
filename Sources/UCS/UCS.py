# – “#” for walls.
# – “ ” (whitespace) for free spaces.
# – “$” for stones.
# – “@” for Ares.
# – “.” for switch places.
# – “*” for stones placed on switches.
# – “+” for Ares on a switch.




from queue import PriorityQueue

class Map:
    def __init__(self, board):
        self.board = board
        self.stone_pos = self.find_stone(board)
        self.switch_pos = self.find_switch(board)
        self.cost = self.Calculate_Board_Cost(board)
        self.Ares = self.find_Ares(board)

    def __lt__(self, other):
        return self.cost < other.cost
    
# Start of class method

    def Is_Complete(self):
    # True if solved
    # False if not solved
        for i in self.board:
            for j in i:
                if self.board[i,j] == "$":
                    return False
        return True

    def find_stone(self):
        # find the location of all stones not in the right position
        result = []
        for i in self.board:
            for j in i:
                if self.board[i,j] == "$":
                    result.append((i,j))
        return result

    def find_switch(self):
        # find the location of all switches without stone on top
        result = []
        for i in self.board:
            for j in i:
                if self.board[i,j] == ".":
                    result.append((i,j))
        return result

    def find_Ares(self):
        # get the position of Player(ares)
        for i in self.board:
            for j in i:
                if self.board[i,j] == "@" or self.board[i,j] == "+":
                    return (i,j)

    def Calculate_Board_Cost(self):
        # calculate the cost of the board
        stone_list = self.find_stone()
        switch_list = self.find_switch()
        return abs(sum(stone_list[i][0] + stone_list[i][1] - switch_list[i][0] - switch_list[i][1] for i in range(len(stone_list))))


def find_next_map(cur_map: Map, visited_Map):
    Ares = cur_map.Ares
    next_map_list = []
    # move up
    if cur_map.board[Ares[0] - 1, Ares[1]] != "#": 
        new_board = cur_map.board

        if new_board[Ares[0], Ares[1]] == "@":
            new_board[Ares[0], Ares[1]] == " "
        elif new_board[Ares[0], Ares[1]] == "+":
            new_board[Ares[0], Ares[1]] == "."

        if new_board[Ares[0] - 1, Ares[1]] == " ":
            new_board[Ares[0] - 1, Ares[1]] = "@"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0] - 1, Ares[1]] == ".":
            new_board[Ares[0] - 1, Ares[1]] = "+"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0] - 1, Ares[1]] == "$":
            if new_board[Ares[0] - 2, Ares[1]] == " ":
                new_board[Ares[0] - 2, Ares[1]] == "$"
                new_board[Ares[0] - 1, Ares[1]] == "@"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0] - 2, Ares[1]] == ".":
                new_board[Ares[0] - 2, Ares[1]] == "*"
                new_board[Ares[0] - 1, Ares[1]] == "@"
                next_map_list.append(Map(new_board))
        elif new_board[Ares[0] - 1, Ares[1]] == "*":
            if new_board[Ares[0] - 2, Ares[1]] == " ":
                new_board[Ares[0] - 2, Ares[1]] == "$"
                new_board[Ares[0] - 1, Ares[1]] == "+"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0] - 2, Ares[1]] == ".":
                new_board[Ares[0] - 2, Ares[1]] == "*"
                new_board[Ares[0] - 1, Ares[1]] == "+"
                next_map_list.append(Map(new_board))


    # move down
    if cur_map.board[Ares[0] + 1, Ares[1]] != "#": 
        new_board = cur_map.board

        if new_board[Ares[0], Ares[1]] == "@":
            new_board[Ares[0], Ares[1]] == " "
        elif new_board[Ares[0], Ares[1]] == "+":
            new_board[Ares[0], Ares[1]] == "."

        if new_board[Ares[0] + 1, Ares[1]] == " ":
            new_board[Ares[0] + 1, Ares[1]] = "@"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0] + 1, Ares[1]] == ".":
            new_board[Ares[0] + 1, Ares[1]] = "+"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0] + 1, Ares[1]] == "$":
            if new_board[Ares[0] + 2, Ares[1]] == " ":
                new_board[Ares[0] + 2, Ares[1]] == "$"
                new_board[Ares[0] + 1, Ares[1]] == "@"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0] + 2, Ares[1]] == ".":
                new_board[Ares[0] + 2, Ares[1]] == "*"
                new_board[Ares[0] + 1, Ares[1]] == "@"
                next_map_list.append(Map(new_board))
        elif new_board[Ares[0] + 1, Ares[1]] == "*":
            if new_board[Ares[0] + 2, Ares[1]] == " ":
                new_board[Ares[0] + 2, Ares[1]] == "$"
                new_board[Ares[0] + 1, Ares[1]] == "+"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0] + 2, Ares[1]] == ".":
                new_board[Ares[0] + 2, Ares[1]] == "*"
                new_board[Ares[0] + 1, Ares[1]] == "+"
                next_map_list.append(Map(new_board))


    # move left
    if cur_map.board[Ares[0], Ares[1] - 1] != "#": 
        new_board = cur_map.board

        if new_board[Ares[0], Ares[1]] == "@":
            new_board[Ares[0], Ares[1]] == " "
        elif new_board[Ares[0], Ares[1]] == "+":
            new_board[Ares[0], Ares[1]] == "."

        if new_board[Ares[0], Ares[1] - 1] == " ":
            new_board[Ares[0], Ares[1] - 1] = "@"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] - 1] == ".":
            new_board[Ares[0], Ares[1] - 1] = "+"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] - 1] == "$":
            if new_board[Ares[0], Ares[1] - 2] == " ":
                new_board[Ares[0], Ares[1] - 2] == "$"
                new_board[Ares[0], Ares[1] - 1] == "@"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0], Ares[1] - 2] == ".":
                new_board[Ares[0], Ares[1] - 2] == "*"
                new_board[Ares[0], Ares[1] - 1] == "@"
                next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] - 1] == "*":
            if new_board[Ares[0], Ares[1] - 2] == " ":
                new_board[Ares[0], Ares[1] - 2] == "$"
                new_board[Ares[0], Ares[1] - 1] == "+"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0], Ares[1] - 2] == ".":
                new_board[Ares[0], Ares[1] - 2] == "*"
                new_board[Ares[0], Ares[1] - 1] == "+"
                next_map_list.append(Map(new_board))

    # move right
    if cur_map.board[Ares[0], Ares[1] + 1] != "#": 
        new_board = cur_map.board

        if new_board[Ares[0], Ares[1]] == "@":
            new_board[Ares[0], Ares[1]] == " "
        elif new_board[Ares[0], Ares[1]] == "+":
            new_board[Ares[0], Ares[1]] == "."

        if new_board[Ares[0], Ares[1] + 1] == " ":
            new_board[Ares[0], Ares[1] + 1] = "@"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] + 1] == ".":
            new_board[Ares[0], Ares[1] + 1] = "+"
            next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] + 1] == "$":
            if new_board[Ares[0], Ares[1] + 2] == " ":
                new_board[Ares[0], Ares[1] + 2] == "$"
                new_board[Ares[0], Ares[1] + 1] == "@"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0], Ares[1] + 2] == ".":
                new_board[Ares[0], Ares[1] + 2] == "*"
                new_board[Ares[0], Ares[1] + 1] == "@"
                next_map_list.append(Map(new_board))
        elif new_board[Ares[0], Ares[1] + 1] == "*":
            if new_board[Ares[0], Ares[1] + 2] == " ":
                new_board[Ares[0], Ares[1] + 2] == "$"
                new_board[Ares[0], Ares[1] + 1] == "+"
                next_map_list.append(Map(new_board))
            elif new_board[Ares[0], Ares[1] + 2] == ".":
                new_board[Ares[0], Ares[1] + 2] == "*"
                new_board[Ares[0], Ares[1] + 1] == "+"
                next_map_list.append(Map(new_board))
    
    
    return next_map_list


def UCS(weightedStone, board):
    start_map = Map(board)

    if start_map.Is_Complete():
        return start_map
    
    visited_map = []
    list_map = PriorityQueue()
    list_map.put(start_map)

    while list_map:
        cur_map: Map = list_map.get()
        visited_map.append(cur_map)
        if cur_map.Is_Complete():
            return cur_map
        
        next_map = find_next_map(cur_map)
        for i in next_map:
            list_map.append(next_map[i])

    pass    