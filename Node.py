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

    def show_information_of_node(board, node, canvas, node_size, color_dictionary):
        if node.state == "visited" or node.state == "path":
            canvas.create_text(node.column * node_size + (node_size / 4), node.row * node_size + (node_size / 5),
                               font=("", math.floor(node_size * 10 / 36)), text=node.distance_to_start, tags=node.state)
            canvas.create_text(node.column * node_size + (node_size * 3 / 4), node.row * node_size + (node_size / 5),
                               font=("", math.floor(node_size * 10 / 36)), text=node.distance_to_finish, tags=node.state)
            canvas.create_text(node.column * node_size + (node_size / 2), node.row * node_size + (node_size * 2 / 3),
                               font=("", math.floor(node_size / 2)), text=node.absolute_weight, tags=node.state)
            neighbors = board.get_neighbors(node)
            unvisited_neighbors = filter(lambda neigh: not neigh.state == "wall", neighbors)
            for neighbor in unvisited_neighbors:
                canvas.create_rectangle(neighbor.column * node_size, neighbor.row * node_size,
                                        neighbor.column * node_size + node_size,
                                        neighbor.row * node_size + node_size,
                                        fill=color_dictionary[neighbor.state], outline="black",
                                        tags=neighbor.state)
                canvas.create_text(neighbor.column * node_size + (node_size / 4),
                                   neighbor.row * node_size + (node_size / 5),
                                   font=("", math.floor(node_size * 10 / 36)), text=neighbor.distance_to_start, tags=neighbor.state)
                canvas.create_text(neighbor.column * node_size + (node_size * 3 / 4),
                                   neighbor.row * node_size + (node_size / 5),
                                   font=("", math.floor(node_size * 10 / 36)), text=neighbor.distance_to_finish, tags=neighbor.state)
                canvas.create_text(neighbor.column * node_size + (node_size / 2),
                                   neighbor.row * node_size + (node_size * 2 / 3),
                                   font=("", math.floor(node_size / 2)), text=neighbor.absolute_weight, tags=neighbor.state)