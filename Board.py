from Node import Node
import math

class Board:
    nodes = None
    startNode = None
    finishNode = None
    def __init__(self, rows, columns):
        self.rows = (rows)
        self.columns = (columns)
        self.nodes = [[Node(row, column, "node", math.inf) for column in
                      range(self.columns)] for row in range(self.rows)]

        self.startRow = math.floor(self.rows / 2)
        self.startColumn = math.floor(self.columns / 4)
        self.startNode = Node(self.startRow, self.startColumn, "start", 0)
        self.nodes[self.startRow][self.startColumn] = Node(self.startRow, self.startColumn, "start", 0)

        self.finishRow = math.floor(self.rows / 2)
        self.finishColumn = math.floor(self.columns / 4 * 3)
        self.finishNode = Node(self.startRow, self.startColumn, "start", 0)
        self.nodes[self.finishRow][self.finishColumn] = Node(self.finishRow, self.finishColumn, "finish", math.inf)