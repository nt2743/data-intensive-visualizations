import math
import time

from Board import Board
import tkinter
import random
from tkinter import *
from algorithms.Algorithm import shortest_path
from algorithms.Dijkstra import dijkstra
from algorithms.A_Star import a_star
from algorithms.Quicksort import quicksort_recursive
from algorithms.Settings import set_global_delay, get_global_delay
from queue import PriorityQueue

root = tkinter.Tk()
root.title("Pathfinding Visualization")
root.state("zoomed") # window full-screen
state = "editable" # represents the current program state

canvas_height = 500
canvas_width = 1530
canvas = Canvas(root, height=canvas_height, width=canvas_width)

# pathfinding variables
node_size = 30
board_rows = math.floor(canvas_height / node_size)
board_columns = math.floor(canvas_width / node_size)
main_board = Board(board_rows, board_columns)
color_dictionary = {
    "node": "white",
    "wall": "grey",
    "start": "red",
    "finish": "green",
    "visited": "cyan",
    "path": "yellow"
}
show_information = False

# sorting variables
sorting_data = list(range(1, 101))
random.shuffle(sorting_data)
element_ids = {}

def select_algorithm(event):
    canvas.delete("all")
    if algorithms.get() == "Dijkstra" or algorithms.get() == "A*":
        node_size_slider.set(node_size)
        draw_board(main_board)
    else:
        draw_sorting_data(sorting_data)

def draw_board(board):
    for row in range(len(board.nodes)):
        for column in range(len(board.nodes[0])):
            node_state = board.nodes[row][column].state
            canvas.create_rectangle(column * node_size,
                                    row * node_size,
                                    column * node_size + node_size,
                                    row * node_size + node_size,
                                    fill=color_dictionary[node_state], outline="black", tags=node_state)
            #if show_information:
               #board.nodes[row][column].show_information_of_node(main_board, canvas, node_size, color_dictionary)

def draw_sorting_data(data):
    global element_ids
    for element in range(len(data)):
        element_id = canvas.create_rectangle(element * canvas_width / len(data),
                                canvas_height,
                                (element+1) * canvas_width / len(data),
                                canvas_height - (canvas_height / len(data) * (data[element])),
                                fill="black", outline="white", tags=data[element])
        element_ids[element] = element_id
        #canvas.create_text(element * canvas_width / len(data),
                                #5,
                                #font=("",7),
                                #text=canvas.gettags(element_id))

def change_node_state(node, new_node_state):
    node.state = new_node_state
    canvas.create_rectangle(node.column * node_size,
                            node.row * node_size,
                            node.column * node_size + node_size,
                            node.row * node_size + node_size,
                            fill=color_dictionary[new_node_state], outline="black", tags=new_node_state)

# build walls
def begin_wall_building(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if not (current_node.state == "node" or current_node.state == "visited" or current_node.state == "path") or state == "visualizing": return
    state = "wall building"
    change_node_state(current_node, "wall")

def build_walls(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if not (current_node.state == "node" or current_node.state == "visited" or current_node.state == "path") or state != "wall building": return
    change_node_state(current_node, "wall")

def complete_wall_building(event):
    global state
    if state == "wall building":
        state = "editable"

# delete walls
def begin_wall_deleting(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if current_node.state != "wall" or state == "visualizing": return
    state = "wall deleting"
    change_node_state(current_node, "node")

def delete_walls(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if current_node.state != "wall" or state != "wall deleting": return
    change_node_state(current_node, "node")

def complete_wall_deleting(event):
    global state
    if state == "wall deleting":
        state = "editable"

# move start and end
def pick(event):
    global state
    if state == "visualizing": return
    state = "moving start or finish"

def drag_start(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if current_node.state != "node" or state != "moving start or finish": return
    current_start = main_board.nodes[main_board.start_row][main_board.start_column]
    change_node_state(current_node, "start")
    change_node_state(current_start, "node")
    main_board.start_row = current_node.row
    main_board.start_column = current_node.column
    main_board.start_node = current_node

def drag_finish(event):
    global state
    try: current_node = main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)]
    except: return
    if current_node.state != "node" or state != "moving start or finish": return
    current_finish = main_board.nodes[main_board.finish_row][main_board.finish_column]
    change_node_state(current_node, "finish")
    change_node_state(current_finish, "node")
    main_board.finish_row = current_node.row
    main_board.finish_column = current_node.column
    main_board.finish_node = current_node

def drop(event):
    global state
    if state == "moving start or finish":
        state = "editable"

# algorithms
next_step = False

def animate_algorithm ():
    global state
    state = "visualizing"
    match algorithms.get():
        case "Dijkstra":
            path_length.set("Weglänge: ...")
            main_board.reset_after_algorithm()
            draw_board(main_board)
            unvisited_nodes = [j for sub in main_board.nodes for j in sub]
            dijkstra(main_board, unvisited_nodes, canvas, node_size, show_information, color_dictionary)
        case "A*":
            path_length.set("Weglänge: ...")
            main_board.reset_after_algorithm()
            draw_board(main_board)
            start_node = main_board.nodes[main_board.start_row][main_board.start_column]
            priority_queue = PriorityQueue()
            priority_queue.put(start_node.absolute_weight, start_node.distance_to_finish, start_node)
            print(priority_queue.get()[2])
            open_set_hash = {start_node}
            a_star(main_board, priority_queue, open_set_hash, canvas, node_size, show_information, color_dictionary)
        case "Quicksort":
            quicksort_recursive(sorting_data, 0, len(sorting_data) - 1, canvas, element_ids)
            canvas.update()

def animate_maze(board, animation_type):
    global state
    if animation_type == "recursive division maze":
        reset_board(board)
        border = main_board.create_border()
        #visualize(main_board, main_board.create_maze_board(2, main_board.rows - 3, 2, main_board.columns - 3, border), "grey", "wall")

        maze = main_board.create_maze_board(2, main_board.rows - 3, 2, main_board.columns - 3, border)

        for node in maze:
            if node.state == "wall":
                canvas.create_rectangle(node.column * node_size,
                                        node.row * node_size,
                                        node.column * node_size + node_size,
                                        node.row * node_size + node_size,
                                        fill="grey", outline="black", tags="wall")
                canvas.update()
                time.sleep(get_global_delay())

        state = "editable"

def visualize (board, nodes_in_order, color, node_state):
    global state, animation_mode, show_information
    node = nodes_in_order.pop(0)
    state = "visualizing"
    if node.state == node_state:
        canvas.create_rectangle(node.column * node_size, node.row * node_size, node.column * node_size + node_size, node.row * node_size + node_size, fill=color, outline="black", tags=node_state)
        # shows the current node weights when animating an algorithm
        if node.state == "node" and show_information:
            canvas.create_text(node.column * node_size + (node_size / 4), node.row * node_size + (node_size / 5),
                        font=("", math.floor(node_size * 10 / 36)), text=node.distance_to_start)
            canvas.create_text(node.column * node_size + (node_size * 3 / 4), node.row * node_size + (node_size / 5),
                        font=("", math.floor(node_size * 10 / 36)), text=node.distance_to_finish)
            canvas.create_text(node.column * node_size + (node_size / 2), node.row * node_size + (node_size * 2 / 3),
                        font=("", math.floor(node_size / 2)), text=node.absolute_weight)
            neighbors = board.get_neighbors(node)
            unvisited_neighbors = filter(lambda neigh: not neigh.state == "wall", neighbors)
            for neighbor in unvisited_neighbors:
                canvas.create_text(neighbor.column * node_size + (node_size / 4), neighbor.row * node_size + (node_size / 5),
                                   font=("", math.floor(node_size * 10 / 36)), text=neighbor.distance_to_start)
                canvas.create_text(neighbor.column * node_size + (node_size * 3 / 4),
                                   neighbor.row * node_size + (node_size / 5),
                                   font=("", math.floor(node_size * 10 / 36)), text=neighbor.distance_to_finish)
                canvas.create_text(neighbor.column * node_size + (node_size / 2),
                                   neighbor.row * node_size + (node_size * 2 / 3),
                                   font=("", math.floor(node_size / 2)), text=neighbor.absolute_weight)

    if len(nodes_in_order) > 0:
        if animation_mode != "step by step" or color == "yellow":
            if animation_mode == "complete":
                root.after(animation_speed_slider.get(), visualize, board, nodes_in_order, color, node_state)
            else:
                root.after(0, visualize, board, nodes_in_order, color, node_state)
    else:
        if color == "cyan":
            print("bla")
            nodes_shortest_path = shortest_path(board, board.finish_node)
            path_length.set("Weglänge: " + str(len(nodes_shortest_path)))
            visualize(board, nodes_shortest_path, "yellow", "node")
        state = "visualized"
        if animation_mode == "skip":
            animation_mode = "complete"

def set_show_information():
    global animation_mode, show_information
    if show_information:
        show_information_text.set("Nodeinformationen anzeigen")
        show_information = False
        draw_board(main_board)
    else:
        show_information_text.set("Nodeinformationen verbergen")
        show_information = True
        draw_board(main_board)

animation_mode = "complete"
def set_animation_mode():
    global animation_mode, debug_button_text
    if animation_mode == "step by step":
        debug_button_text.set("Visualisierung: komplett")
        animation_mode = "complete"
    else:
        debug_button_text.set("Visualisierung: Schritt für Schritt")
        animation_mode = "step by step"

def update_delay(new_delay):
    set_global_delay(float(new_delay) / 1000)

def skip_animation():
    global animation_mode
    if animation_mode == "complete":
        animation_mode = "skip"

    set_global_delay(0)

def reset_board(board):
    global main_board, board_rows, board_columns, state
    canvas.delete("all")
    board_rows = math.floor(canvas_height / node_size)
    board_columns = math.floor(canvas_width / node_size)
    main_board = Board(board_rows, board_columns)
    draw_board(main_board)
    state = "editable"

def delete_paths(board):
    board.reset_after_algorithm()
    draw_board(main_board)

def create_random_maze():
    reset_board(main_board)
    main_board.create_random_maze_board()
    draw_board(main_board)

selected_node = main_board.nodes[0][0]
def display_node_information(event):
    global node_information, selected_node
    try:
        canvas.create_rectangle(selected_node.column * node_size + 1, selected_node.row * node_size + 1,
                                selected_node.column * node_size + node_size - 1,
                                selected_node.row * node_size + node_size - 1, outline=color_dictionary[selected_node.state])
        current_row = math.floor(event.y / node_size)
        current_column = math.floor(event.x / node_size)

        selected_node = main_board.nodes[current_row][current_column]
        node_information.set("Row: " + str(selected_node.row) + "\nColumn: " + str(selected_node.column) + "\nDistance to start: " + str(selected_node.distance_to_start) +
                             "\nDistance to finish: " + str(selected_node.distance_to_finish) +
                             "\nAbsolute weight: " + str(selected_node.absolute_weight))
        canvas.create_rectangle(selected_node.column * node_size + 1, selected_node.row * node_size + 1, selected_node.column * node_size + node_size - 1,
                                selected_node.row * node_size + node_size - 1, outline="black")
    except:
        return

def set_node_size(event):
    global node_size
    node_size = node_size_slider.get()
    reset_board(main_board)
    draw_board(main_board)

canvas.tag_bind("node", "<Button-1>", begin_wall_building)
canvas.tag_bind("node", "<Motion>", build_walls)
canvas.tag_bind("node", "<ButtonRelease-1>", complete_wall_building)

canvas.tag_bind("visited", "<Button-1>", begin_wall_building)
canvas.tag_bind("visited", "<Motion>", build_walls)
canvas.tag_bind("visited", "<ButtonRelease-1>", complete_wall_building)

canvas.tag_bind("path", "<Button-1>", begin_wall_building)
canvas.tag_bind("path", "<Motion>", build_walls)
canvas.tag_bind("path", "<ButtonRelease-1>", complete_wall_building)

canvas.tag_bind("wall", "<Button-1>", begin_wall_deleting)
canvas.tag_bind("wall", "<Motion>", delete_walls)
canvas.tag_bind("wall", "<ButtonRelease-1>", complete_wall_deleting)

canvas.tag_bind("start", "<Button-1>", pick)
canvas.tag_bind("start", "<Motion>", drag_start)
canvas.tag_bind("start", "<ButtonRelease-1>", drop)

canvas.tag_bind("finish", "<Button-1>", pick)
canvas.tag_bind("finish", "<Motion>", drag_finish)
canvas.tag_bind("finish", "<ButtonRelease-1>", drop)

canvas.tag_bind("node", "<Enter>", display_node_information)
canvas.tag_bind("wall", "<Enter>", display_node_information)
canvas.tag_bind("start", "<Enter>", display_node_information)
canvas.tag_bind("finish", "<Enter>", display_node_information)
canvas.tag_bind("visited", "<Enter>", display_node_information)
canvas.tag_bind("path", "<Enter>", display_node_information)
canvas.pack()

node_information = tkinter.StringVar()
node_information.set("Row: \nColumn:\n Distance to start:\n Distance to finish: ")
node_information_label = Label(root, textvariable=node_information, bg="#D0D0D0", font=("Helvatical bold",20), justify="left")
node_information_label.pack(side="left")


node_size_label = Label(root, text="Größe der Nodes")
node_size_label.pack(anchor=NE)
node_size_slider = Scale(root, from_=10, to=50, orient=HORIZONTAL, command=set_node_size)
node_size_slider.pack(side="right", anchor=NE)

clear_board = tkinter.Button(root, text="Zurücksetzen", command=lambda: reset_board(main_board))
clear_board.pack(side="right", anchor=NE)

clear_paths = tkinter.Button(root, text="Wege entfernen", command=lambda: delete_paths(main_board))
clear_paths.pack(side="right", anchor=NE)

recursive_maze = tkinter.Button(root, text="Labyrinth erzeugen", command=lambda: animate_maze(main_board, "recursive division maze"))
recursive_maze.pack(side="right", anchor=NE)

random_maze = tkinter.Button(root, text="Zufälliges Labyrinth erzeugen", command=lambda: create_random_maze())
random_maze.pack(side="right", anchor=NE)


start_algorithm = tkinter.Button(root, text="Algorithmus starten", command=lambda: animate_algorithm())
start_algorithm.pack()

show_information_text = tkinter.StringVar()
show_information_text.set("Nodeinformationen anzeigen")
set_show_information_button = tkinter.Button(root, textvariable=show_information_text, command=lambda: set_show_information())
set_show_information_button.pack()

algorithms = StringVar(root)
algorithms.set("Quicksort") # default value

choose_algorithm = OptionMenu(root, algorithms, "Dijkstra", "A*", "Quicksort", command=select_algorithm)
choose_algorithm.pack()
select_algorithm("")

path_length = tkinter.StringVar()
path_length.set("")
path_length_label = Label(root, textvariable=path_length)
path_length_label.pack()

animation_speed_label = Label(root, text="Geschwindigkeit der Animation")
animation_speed_label.pack()
animation_speed_slider = Scale(root, from_=50, to=1, orient=HORIZONTAL, command=update_delay, showvalue=False)
animation_speed_slider.pack(fill="x")
animation_speed_slider.set(25)
animation_speed_slider.pack()

skip_animation_button = tkinter.Button(root, text="Animation überspringen", command=lambda: skip_animation())
skip_animation_button.pack()

root.mainloop()