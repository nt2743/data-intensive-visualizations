import math

class Node:
    state = "node"
    isVisited = False
    previousNode = None
    distance_to_finish = math.inf
    def __init__(self, row, column, state, distance_to_start):
        self.row = row
        self.column = column
        self.state = state
        self.distance_to_start = distance_to_start

    def __lt__(self, other):
        #if (self.distance_to_finish + self.distance_to_start) == (other.distance_to_finish + other.distance_to_start):
        return self.distance_to_finish < other.distance_to_finish
        #return (self.distance_to_finish + self.distance_to_start) < (other.distance_to_finish + other.distance_to_start)