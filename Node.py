import math

class Node:
    state = "node"
    is_visited = False
    previous_node = None
    distance_to_finish = math.inf
    def __init__(self, row, column, state):
        self.row = row
        self.column = column
        self.state = state

    @property
    def distance_to_start(self):
        if self.state == "start": return 0
        if self.previous_node is None: return math.inf
        return self.previous_node.distance_to_start + 1

    @property
    def absolute_weight(self):
        return self.distance_to_start + self.distance_to_finish

    def __lt__(self, other):
        if self.absolute_weight == other.absolute_weight:
            return self.distance_to_finish < other.distance_to_finish
        return self.absolute_weight < other.absolute_weight