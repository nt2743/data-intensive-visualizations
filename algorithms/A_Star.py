import math
import time
from algorithms.Settings import get_global_delay
from Board import shortest_path

def a_star(board, priority_queue, open_set_hash, canvas, node_size, show_information, color_dictionary):
    # no possible way to finish
    if priority_queue.empty():
        return

    current_node = priority_queue.get()[2]
    open_set_hash.remove(current_node)

    # check if done
    if current_node == board.finish_node:
        shortest_path(board, board.finish_node, 0, canvas, node_size, show_information, color_dictionary)
        return


    # update nodes
    current_node.is_visited = True
    priority_queue = update_neighbors(current_node, board, priority_queue, open_set_hash)

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
        if show_information:
            current_node.show_information_of_node(board, current_node, canvas, node_size, color_dictionary)

    # recursive step
    a_star(board, priority_queue, open_set_hash, canvas, node_size, show_information, color_dictionary)

def update_neighbors(node, board, queue, open_set_hash):
	neighbors = board.get_neighbors(node)
	for neighbor in neighbors:
		if neighbor.state == "wall":
			continue
		board.calculate_distance_to_finish(neighbor)
		if node.distance_to_start + 1 < neighbor.distance_to_start:
			neighbor.previous_node = node # also sets distance_to_start
			if neighbor not in open_set_hash:
				queue.put((neighbor.absolute_weight, neighbor.distance_to_finish, neighbor))
				open_set_hash.add(neighbor)
				neighbor.is_visited = False

	if node != board.start_node:
		node.is_visited = True
	return queue