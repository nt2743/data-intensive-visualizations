def update_unvisited_neighbors(node, board):
    neighbors = board.get_neighbors(node)
    for neighbor in neighbors:
        if not neighbor.is_visited and neighbor.state != "wall":
            neighbor.previous_node = node