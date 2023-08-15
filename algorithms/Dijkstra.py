import math
import time
from algorithms.Settings import get_global_delay
from Board import shortest_path

def dijkstra (board, unvisited_nodes, canvas, node_size, show_information, color_dictionary):
    unvisited_nodes.sort(key=lambda node: node.distance_to_start)
    current_node = unvisited_nodes.pop(0)
    # no possible way to finish
    if current_node.distance_to_start == math.inf:
        return

    # check if done
    if current_node == board.finish_node:
        shortest_path(board, board.finish_node, 0, canvas, node_size, show_information, color_dictionary)
        return

    # draw visited node
    if current_node.state == "node":
        current_node.state = "visited"
        if get_global_delay() != 0:
            canvas.create_rectangle(current_node.column * node_size,
                                current_node.row * node_size,
                                current_node.column * node_size + node_size,
                                current_node.row * node_size + node_size,
                                fill=color_dictionary[current_node.state], outline="black", tags=current_node.state)
            canvas.update()
            time.sleep(get_global_delay())
        #if show_information:
            #current_node.show_information_of_node(board, canvas, node_size, color_dictionary)

    # update nodes
    current_node.is_visited = True
    update_unvisited_neighbors(current_node, board)

    # recursive step
    dijkstra(board, unvisited_nodes, canvas, node_size, show_information, color_dictionary)

def update_unvisited_neighbors(node, board):
    neighbors = board.get_neighbors(node)
    for neighbor in neighbors:
        if not neighbor.is_visited and neighbor.state != "wall":
            neighbor.previous_node = node