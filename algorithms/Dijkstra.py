import math
from Board import Board

def get_unvisited_neighbors(node, nodes):
  neighbors = []
  row = node.row
  column = node.column
  if row > 0: neighbors.append(nodes[row - 1][column])
  if row < len(nodes) - 1: neighbors.append(nodes[row + 1][column])
  if column > 0: neighbors.append(nodes[row][column - 1]);
  if column < len(nodes[0]) - 1: neighbors.append(nodes[row][column + 1]);
  return filter(lambda neighbor: not neighbor.isVisited, neighbors)

def update_unvisited_neighbors(node, nodes):
  unvisited_neighbors = get_unvisited_neighbors(node, nodes)
  for neighbor in unvisited_neighbors:
    neighbor.distance = node.distance + 1
    neighbor.previousNode = node

def check_if_done(node, finish_row, finish_column):
    if node.row == finish_row and node.column == finish_column:
        return True
    return False

def dijkstra (board):
    visited_nodes = []
    unvisited_nodes = [j for sub in board.nodes for j in sub]
    closest_node = None
    while len(unvisited_nodes) > 0:
        unvisited_nodes.sort(key=lambda node: node.distance)
        closest_node = unvisited_nodes.pop(0)
        if closest_node.state == "wall":
            continue
        if closest_node.distance == math.inf:
            return visited_nodes
        closest_node.isVisited = True
        visited_nodes.append(closest_node)
        if check_if_done(closest_node, board.finishRow, board.finishColumn):
            return visited_nodes
        update_unvisited_neighbors(closest_node, board.nodes)
    return visited_nodes