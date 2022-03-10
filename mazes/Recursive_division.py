import random, math


maze = []

def create_maze_board(board, row_start, row_end, column_start, column_end, iteration):
    iteration+=1
    print(iteration)
    global maze
    if row_end < row_start or column_end < column_start:
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
    possible_walls = []
    possible_walls.append(random_start_point)
    for number in range(random_start_point, random_end_point, 2):
        possible_walls.append(number)

    # for picking the open path
    possible_paths = []
    possible_paths.append(random_start_open_spot - 1)
    for number in range(random_start_open_spot - 1, random_end_open_spot + 1, 2):
        possible_paths.append(number)

    random_wall_index = math.floor(random.uniform(0, len(possible_walls)))
    random_path_index = math.floor(random.uniform(0, len(possible_paths)))
    try:
        random_spot_to_build_wall = possible_walls[random_wall_index]
    except:
        print("doesnt work")

    open_spot = possible_paths[random_path_index]

    #### 1 19 1 39
    #random_spot_to_build_wall = random.randint(math.floor(random_start_point / 2), math.floor(random_end_point / 2)) * 2
    ####random_spot_to_build_wall = random.randrange(random_start_point, random_end_point, 2)

    #open_spot = math.floor(random.uniform(random_start_open_spot, random_end_open_spot))

    # build the wall
    for node in range(random_start_open_spot - 1, random_end_open_spot + 2):
        if is_horizontal:
            if not (board.nodes[random_spot_to_build_wall][node].state == "start" or board.nodes[random_spot_to_build_wall][node].state == "finish"):
                board.nodes[random_spot_to_build_wall][node].state = "wall"
                maze.append(board.nodes[random_spot_to_build_wall][node])
        else:
            if not (board.nodes[node][random_spot_to_build_wall].state == "start" or board.nodes[node][random_spot_to_build_wall].state == "finish"):
                board.nodes[node][random_spot_to_build_wall].state = "wall"
                maze.append(board.nodes[node][random_spot_to_build_wall])

    # recursion
    #if is_horizontal:
        #board.nodes[random_spot_to_build_wall][open_spot].state = "node"
        #print("path:", open_spot)
        #create_maze_board(board, row_start, random_spot_to_build_wall - 1, column_start, column_end, iteration)
        #create_maze_board(board, random_spot_to_build_wall + 1, row_end, column_start, column_end, iteration)
    #else:
        #board.nodes[open_spot][random_spot_to_build_wall].state = "node"
        #print("path:", open_spot)
        #create_maze_board(board, row_start, row_end, column_start, random_spot_to_build_wall - 1, iteration)
        #create_maze_board(board, row_start, row_end, random_spot_to_build_wall + 1, column_end, iteration)

    if is_horizontal:
        board.nodes[random_spot_to_build_wall][open_spot].state = "node"
        create_maze_board(board, row_start, random_spot_to_build_wall - 2, column_start, column_end, iteration)
        create_maze_board(board, random_spot_to_build_wall + 2, row_end, column_start, column_end, iteration)
    else:
        board.nodes[open_spot][random_spot_to_build_wall].state = "node"
        create_maze_board(board, row_start, row_end, column_start, random_spot_to_build_wall - 2, iteration)
        create_maze_board(board, row_start, row_end, random_spot_to_build_wall + 2, column_end, iteration)
    return maze