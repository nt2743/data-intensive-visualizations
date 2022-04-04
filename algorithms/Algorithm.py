#class Algorithm:
def shortest_path(board):
    nodes_shortest_path = []
    current_node = board.nodes[board.finish_row][board.finish_column]
    while current_node is not None:
        nodes_shortest_path.append(current_node)
        current_node = current_node.previous_node
    return nodes_shortest_path