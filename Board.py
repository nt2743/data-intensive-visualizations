from Node import Node
import math

class Board:
    def __init__(self, rows, columns):
        self.rows = (rows)
        self.columns = (columns)
        self.nodes = [[Node(row, column, "node", math.inf) for column in
                      range(self.columns)] for row in range(self.rows)]

        self.startRow = math.floor(self.rows / 2)
        self.startColumn = math.floor(self.columns / 4)
        self.nodes[self.startRow][self.startColumn] = Node(self.startRow, self.startColumn, "start", 0)

        self.finishRow = math.floor(self.rows / 2)
        self.finishColumn = math.floor(self.columns / 4 * 3)
        self.nodes[self.finishRow][self.finishColumn] = Node(self.finishRow, self.finishColumn, "finish", math.inf)

    def create_labyrinth_board(self):
        for column in range (self.columns):
            self.nodes[0][column].state = "wall"
            self.nodes[self.rows-1][column].state = "wall"