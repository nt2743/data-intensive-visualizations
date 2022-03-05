class Node:
    state = "node"
    isVisited = False
    previousNode = None
    def __init__(self, row, column, state, distance):
        self.row = row
        self.column = column
        self.state = state
        self.distance = distance