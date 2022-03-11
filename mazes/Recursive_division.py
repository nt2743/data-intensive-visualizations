import random, math


def create_maze_board(board, row_start, row_end, column_start, column_end, maze):
    if row_end < row_start-1 or column_end < column_start-1:
        return

    # decide if the wall will be horizontal or vertical
    if row_end - row_start > column_end - column_start:
        is_horizontal = True
        random_start_open_spot = column_start
        random_end_open_spot = column_end
        random_start_point = row_start
        random_end_point = row_end
    else:
        is_horizontal = False
        random_start_open_spot = row_start
        random_end_open_spot = row_end
        random_start_point = column_start
        random_end_point = column_end

    # for building the wall
    possible_walls = [random_start_point]
    for number in range(random_start_point, random_end_point, 2):
        possible_walls.append(number)

    # for picking the open path
    possible_paths = [random_start_open_spot - 1]
    for number in range(random_start_open_spot - 1, random_end_open_spot + 1, 2):
        possible_paths.append(number)

    random_wall_index = math.floor(random.uniform(0, len(possible_walls)))
    random_path_index = math.floor(random.uniform(0, len(possible_paths)))
    random_spot_to_build_wall = possible_walls[random_wall_index]

    open_spot = possible_paths[random_path_index]

    # build the wall
    for node in range(random_start_open_spot - 1, random_end_open_spot + 2):
        if is_horizontal:
            if not is_surrounding_start_or_finish(board, random_spot_to_build_wall, node):
                board.nodes[random_spot_to_build_wall][node].state = "wall"
                maze.append(board.nodes[random_spot_to_build_wall][node])
        else:
            if not is_surrounding_start_or_finish(board, node, random_spot_to_build_wall):
                board.nodes[node][random_spot_to_build_wall].state = "wall"
                maze.append(board.nodes[node][random_spot_to_build_wall])

    # recursion
    if is_horizontal:
        board.nodes[random_spot_to_build_wall][open_spot].state = "node"
        create_maze_board(board, row_start, random_spot_to_build_wall - 2, column_start, column_end, maze)
        create_maze_board(board, random_spot_to_build_wall + 2, row_end, column_start, column_end, maze)
    else:
        board.nodes[open_spot][random_spot_to_build_wall].state = "node"
        create_maze_board(board, row_start, row_end, column_start, random_spot_to_build_wall - 2, maze)
        create_maze_board(board, row_start, row_end, random_spot_to_build_wall + 2, column_end, maze)
    return maze

def is_surrounding_start_or_finish(board, current_row, current_column):
    for row in range (current_row - 1, current_row + 2):
        for column in range(current_column - 1, current_column + 2):
            if board.nodes[row][column].state == "start" or board.nodes[row][column].state == "finish":
                return True
    return False