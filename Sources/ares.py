# Direction mappings: key is move letter, value is (dr, dc)
DIRECTIONS = {
    'u': (-1, 0),   #   up
    'd': (1, 0),    #   down
    'l': (0, -1),   #   left
    'r': (0, 1)     #   right
}


class State:
    # Khoi tao
    def __init__(self, ares, stones, path="", cost = 0):
        self.ares = ares        #tuple
        self.stones = stones    #tuple
        self.path = path
        self.cost 
    # So sanh 2 state = hoac !=
    def  __eq__(self, other):
        return self.ares == other.self and self.stones == other.stones

def in_bounds(pos, map):
    x, y = pos
    return 0 <= x < len(map) and 0 <= y < len(map[0])

def winCondition(state, switches):
    for i in state.stones:
        if i not in switches:
            return False
    return True

def starting_state(map):
    ''' We scan the map to identify:
        - Ares position
        - Stones position
        - Switches position
    '''

    ares = None         # ares position 
    stones = []         # stones position list
    switches = set()
    nRow = len(map)
    nCol = len(map[0])

    for x in range(nRow):
        for y in range(nCol):
            c = map[x][y]
            if c == '@' or c == '+':
                ares = (x, y)
            if c == '$' or c == '*':
                stones.append((x, y)) # list
            if c == '.' or c == '*' or c == '+':
                switches.add((x, y)) # set

    state = State(ares, stones)

    # return starting state and switches position
    return state, switches

