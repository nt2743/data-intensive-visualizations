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