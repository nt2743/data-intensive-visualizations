from Node import Node
import math
import random
import time

from algorithms.Settings import get_global_delay

class Board:
    def __init__(self, rows, columns):
        self.rows = (rows)
        self.columns = (columns)
        self.nodes = [[Node(row, column, "node") for column in
                      range(self.columns)] for row in range(self.rows)]

        self.start_row = math.floor(self.rows / 2)
        self.start_column = math.floor(self.columns / 4)
        self.start_node = Node(self.start_row, self.start_column, "start")
        self.nodes[self.start_row][self.start_column] = self.start_node

        self.finish_row = math.floor(self.rows / 2)
        self.finish_column = math.floor(self.columns / 4 * 3)
        self.finish_node = Node(self.finish_row, self.finish_column, "finish")
        self.nodes[self.finish_row][self.finish_column] = self.finish_node

    def get_neighbors(self, node):
        neighbors = []
        row = node.row
        column = node.column
        if row > 0: neighbors.append(self.nodes[row - 1][column])
        if row < self.rows - 1: neighbors.append(self.nodes[row + 1][column])
        if column > 0: neighbors.append(self.nodes[row][column - 1])
        if column < self.columns - 1: neighbors.append(self.nodes[row][column + 1])
        return neighbors

    def calculate_distance_to_finish(self, node):
        node.distance_to_finish = int(math.fabs(self.finish_row - node.row) + math.fabs(self.finish_column - node.column))

    def create_border(self):
        border = []
        for row in range(self.rows):
            self.nodes[row][0].state = "wall"
            border.append(self.nodes[row][0])
            self.nodes[row][self.columns-1].state = "wall"
            border.append(self.nodes[row][self.columns-1])
        for column in range(self.columns):
            self.nodes[0][column].state = "wall"
            border.append(self.nodes[0][column])
            self.nodes[self.rows-1][column].state = "wall"
            border.append(self.nodes[self.rows-1][column])
        return border

    def create_random_maze_board(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.nodes[row][column].state != "start" and self.nodes[row][column].state != "finish":
                    random_number = random.uniform(0, 1)
                    if random_number > 0.7:
                        self.nodes[row][column].state = "wall"
                    else:
                        self.nodes[row][column].state = "node"

    def reset_after_algorithm(self):
        for row in range(self.rows):
            for column in range(self.columns):
                node = self.nodes[row][column]
                node.is_visited = False
                node.previous_node = None
                node.distance_to_finish = math.inf
                if node.state == "visited" or node.state == "path":
                    node.state = "node"

    def create_maze_board(self, row_start, row_end, column_start, column_end, maze):
        if row_end < row_start - 1 or column_end < column_start - 1:
            return

        # decide if the wall will be horizontal or vertical
        if row_end - row_start > column_end - column_start:
            is_horizontal = True
            possible_open_spot_start = column_start
            possible_open_spot_end = column_end
            possible_walls_start = row_start
            possible_walls_end = row_end
        else:
            is_horizontal = False
            possible_open_spot_start = row_start
            possible_open_spot_end = row_end
            possible_walls_start = column_start
            possible_walls_end = column_end

        # for building the wall
        possible_walls = [possible_walls_start]
        for number in range(possible_walls_start + 2, possible_walls_end, 2):
            possible_walls.append(number)

        # for picking the open path
        possible_open_spots = [possible_open_spot_start - 1]
        for number in range(possible_open_spot_start + 1, possible_open_spot_end + 1, 2):
            possible_open_spots.append(number)

        random_wall_index = math.floor(random.uniform(0, len(possible_walls)))
        random_path_index = math.floor(random.uniform(0, len(possible_open_spots)))

        spot_to_build_wall = possible_walls[random_wall_index]
        open_spot = possible_open_spots[random_path_index]

        # build the wall
        for node in range(possible_open_spot_start - 1, possible_open_spot_end + 2):
            if is_horizontal:
                if not self.is_surrounding_start_or_finish(spot_to_build_wall, node):
                    self.nodes[spot_to_build_wall][node].state = "wall"
                    maze.append(self.nodes[spot_to_build_wall][node])
            else:
                if not self.is_surrounding_start_or_finish(node, spot_to_build_wall):
                    self.nodes[node][spot_to_build_wall].state = "wall"
                    maze.append(self.nodes[node][spot_to_build_wall])

        # recursion
        if is_horizontal:
            self.nodes[spot_to_build_wall][open_spot].state = "node"
            self.create_maze_board(row_start, spot_to_build_wall - 2, column_start, column_end, maze)
            self.create_maze_board(spot_to_build_wall + 2, row_end, column_start, column_end, maze)
        else:
            self.nodes[open_spot][spot_to_build_wall].state = "node"
            self.create_maze_board(row_start, row_end, column_start, spot_to_build_wall - 2, maze)
            self.create_maze_board(row_start, row_end, spot_to_build_wall + 2, column_end, maze)
        return maze

    def is_surrounding_start_or_finish(self, current_row, current_column):
        for row in range(current_row - 1, current_row + 2):
            for column in range(current_column - 1, current_column + 2):
                if self.nodes[row][column].state == "start" or self.nodes[row][column].state == "finish":
                    return True
        return False

def shortest_path(board, current_node, length, canvas, node_size, show_information, color_dictionary):
    length += 1
    # path_length.set("Weglänge: " + str(length))
    previous_node = current_node.previous_node

    while previous_node != board.start_node:
        previous_node.state = "path"
        canvas.create_rectangle(previous_node.column * node_size, previous_node.row * node_size,
                                previous_node.column * node_size + node_size,
                                previous_node.row * node_size + node_size, fill=color_dictionary[previous_node.state],
                                outline="black", tags=previous_node.state)
        canvas.update()
        time.sleep(get_global_delay())
        if show_information:
            current_node.show_information_of_node(board, current_node, canvas, node_size, color_dictionary)
        previous_node = previous_node.previous_node

    state = "visualized"
    animation_mode = "complete"