import math
from queue import PriorityQueue

def get_unvisited_neighbors(node, board):
    neighbors = []
    row = node.row
    column = node.column
    if row > 0: neighbors.append(board.nodes[row - 1][column])
    if row < len(board.nodes) - 1: neighbors.append(board.nodes[row + 1][column])
    if column > 0: neighbors.append(board.nodes[row][column - 1]);
    if column < len(board.nodes[0]) - 1: neighbors.append(board.nodes[row][column + 1]);
    return filter(lambda neighbor: not neighbor.isVisited, neighbors)

def update_unvisited_neighbors(node, board, unvisited_nodes):
    unvisited_neighbors = get_unvisited_neighbors(node, board)
    for neighbor in unvisited_neighbors:
        neighbor.distance_to_start = node.distance_to_start + 1
        neighbor.previousNode = node
        board.calculate_distance_to_finish(node)
        unvisited_nodes.put(neighbor)
        #print(unvisited_nodes.get()[1])
    return unvisited_nodes


def check_if_done(node, finish_row, finish_column):
    if node.row == finish_row and node.column == finish_column:
        return True
    return False

def a_star (board):
    visited_nodes = []
    unvisited_nodes = PriorityQueue()
    unvisited_nodes.put(board.nodes[board.start_row][board.start_column])
    while unvisited_nodes.qsize() > 0:
        closest_node = unvisited_nodes.get()
        if closest_node.state == "wall":
            continue
        if closest_node.distance_to_start == math.inf:
            return visited_nodes
        closest_node.isVisited = True
        visited_nodes.append(closest_node)
        if check_if_done(closest_node, board.finish_row, board.finish_column):
            return visited_nodes
        unvisited_nodes = update_unvisited_neighbors(closest_node, board, unvisited_nodes)
    return visited_nodes

def shortest_path(board):
    nodes_shortest_path = []
    current_node = board.nodes[board.finish_row][board.finish_column]
    while current_node != None:
        nodes_shortest_path.append(current_node)
        current_node = current_node.previousNode
    return nodes_shortest_path