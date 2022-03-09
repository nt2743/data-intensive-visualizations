import random, math


maze = []

def create_maze_board(board, row_start, row_end, column_start, column_end):
    global maze
    if row_end - row_start < 2 or column_end - column_start < 2:
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

    random_spot_to_build_wall = math.floor(random.uniform(random_start_point, random_end_point))

    if is_horizontal and (random_spot_to_build_wall == board.startRow or random_spot_to_build_wall == board.finishRow):
        create_maze_board(board, row_start, row_end, column_start, column_end)
        return
    if not is_horizontal and (random_spot_to_build_wall == board.startColumn or random_spot_to_build_wall == board.finishColumn):
        create_maze_board(board, row_start, row_end, column_start, column_end)
        return
    open_spot = math.floor(random.uniform(random_start_open_spot, random_end_open_spot))

    for node in range(random_start_open_spot, random_end_open_spot):
        if is_horizontal:
            board.nodes[random_spot_to_build_wall][node].state = "wall"
            maze.append(board.nodes[random_spot_to_build_wall][node])
        else:
            board.nodes[node][random_spot_to_build_wall].state = "wall"
            maze.append(board.nodes[node][random_spot_to_build_wall])

    if is_horizontal:
        board.nodes[random_spot_to_build_wall][open_spot].state = "node"
        create_maze_board(board, row_start, random_spot_to_build_wall, column_start, column_end)
        create_maze_board(board, random_spot_to_build_wall + 1, row_end, column_start, column_end)
    else:
        board.nodes[open_spot][random_spot_to_build_wall].state = "node"
        create_maze_board(board, row_start, row_end, column_start, random_spot_to_build_wall)
        create_maze_board(board, row_start, row_end, random_spot_to_build_wall + 1, column_end)
    return maze