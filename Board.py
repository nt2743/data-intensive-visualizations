from Node import Node
import math
import random

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

    def create_maze_board(self):
        for column in range (self.columns):
            self.nodes[0][column].state = "wall"
            self.nodes[self.rows-1][column].state = "wall"

    def create_random_maze_board(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.nodes[row][column].state != "start" and self.nodes[row][column].state != "finish":
                    random_number = random.uniform(0, 1)
                    if random_number > 0.6:
                        self.nodes[row][column].state = "wall"
                    else:
                        self.nodes[row][column].state = "node"