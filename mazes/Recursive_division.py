import random, math


def create_maze_board(board, row_start, row_end, column_start, column_end, maze):
    if row_end < row_start-1 or column_end < column_start-1:
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
            if not is_surrounding_start_or_finish(board, spot_to_build_wall, node):
                board.nodes[spot_to_build_wall][node].state = "wall"
                maze.append(board.nodes[spot_to_build_wall][node])
        else:
            if not is_surrounding_start_or_finish(board, node, spot_to_build_wall):
                board.nodes[node][spot_to_build_wall].state = "wall"
                maze.append(board.nodes[node][spot_to_build_wall])

    # recursion
    if is_horizontal:
        board.nodes[spot_to_build_wall][open_spot].state = "node"
        create_maze_board(board, row_start, spot_to_build_wall - 2, column_start, column_end, maze)
        create_maze_board(board, spot_to_build_wall + 2, row_end, column_start, column_end, maze)
    else:
        board.nodes[open_spot][spot_to_build_wall].state = "node"
        create_maze_board(board, row_start, row_end, column_start, spot_to_build_wall - 2, maze)
        create_maze_board(board, row_start, row_end, spot_to_build_wall + 2, column_end, maze)
    return maze

def is_surrounding_start_or_finish(board, current_row, current_column):
    for row in range (current_row - 1, current_row + 2):
        for column in range(current_column - 1, current_column + 2):
            if board.nodes[row][column].state == "start" or board.nodes[row][column].state == "finish":
                return True
    return False