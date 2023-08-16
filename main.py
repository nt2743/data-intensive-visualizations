import math
import time

from Board import Board
import tkinter
import random
from tkinter import *
from algorithms.Algorithm import shortest_path
from algorithms.Dijkstra import dijkstra
from algorithms.A_Star import a_star
from algorithms.Quicksort import quicksort_recursive, comparisons, swaps
from algorithms import Quicksort
from algorithms.Settings import set_global_delay, get_global_delay
from queue import PriorityQueue

root = tkinter.Tk()
root.title("Pathfinding Visualization")
root.state("zoomed") # window full-screen
state = "editable" # represents the current program state

canvas_height = 550
canvas_width = 1530
canvas = Canvas(root, height=canvas_height, width=canvas_width)

# pathfinding variables
node_size = 35
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
element_ids = {}

def select_algorithm(event):
    global node_size, sorting_data
    canvas.delete("all")
    if algorithms.get() == "Dijkstra" or algorithms.get() == "A*":
        recursive_maze_and_worst_case.config(text="Create recursive maze")
        randomize.config(text="Create random walls")
        element_information.set("Node Information \nRow: \nColumn: \nDistance to start: \nDistance to finish: \nAbsolute weight: ")
        node_size = data_amount_slider.get()
        reset("")
        draw_board(main_board)
        data_amount.set("Amount of nodes: " + str((main_board.rows-1)*(main_board.columns-1)))
        algorithm_information.set("visited nodes: 0      path length: 0       ")
    else:
        recursive_maze_and_worst_case.config(text="Create worst case")
        randomize.config(text="Shuffle")
        element_information.set("Element Information \nPosition: \nValue: ")
        sorting_data = list(range(1, 200-data_amount_slider.get()*3))
        random.shuffle(sorting_data)
        draw_sorting_data(sorting_data)
        data_amount.set("Amount of elements: " + str(200-data_amount_slider.get() * 3 - 1))
        algorithm_information.set("comparisons: 0       swaps: 0     ")

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
                                fill="black", outline="white", tags=(str(element+1), str(data[element])))
        element_ids[element] = element_id
        canvas.tag_bind(element_id, "<Enter>", display_element_information)

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
            main_board.reset_after_algorithm()
            draw_board(main_board)
            unvisited_nodes = [j for sub in main_board.nodes for j in sub]
            dijkstra(main_board, unvisited_nodes, canvas, node_size, show_information, color_dictionary, algorithm_information, 0)
            draw_board(main_board)
        case "A*":
            main_board.reset_after_algorithm()
            draw_board(main_board)
            start_node = main_board.nodes[main_board.start_row][main_board.start_column]
            priority_queue = PriorityQueue()
            priority_queue.put((start_node.absolute_weight, start_node.distance_to_finish, start_node))
            open_set_hash = {start_node}
            a_star(main_board, priority_queue, open_set_hash, canvas, node_size, show_information, color_dictionary, algorithm_information, 0)
            draw_board(main_board)
        case "Quicksort":
            quicksort_recursive(sorting_data, 0, len(sorting_data) - 1, canvas, element_ids, algorithm_information)
            Quicksort.comparisons = 0
            Quicksort.swaps = 0
            canvas.update()

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
    delay_information.set("delay: " + new_delay + "ms")

def skip_animation():
    global animation_mode
    if animation_mode == "complete":
        animation_mode = "skip"

    set_global_delay(0)

def reset(event):
    global main_board, board_rows, board_columns, state, node_size
    if algorithms.get() == "Dijkstra" or algorithms.get() == "A*":
        canvas.delete("all")
        node_size = data_amount_slider.get()
        board_rows = math.floor(canvas_height / node_size)
        board_columns = math.floor(canvas_width / node_size)
        main_board = Board(board_rows, board_columns)
        draw_board(main_board)
        state = "editable"
        data_amount.set("Amount of nodes: " + str((main_board.rows - 1) * (main_board.columns - 1)))
        algorithm_information.set("visited nodes: 0      path length: 0       ")
    else:
        select_algorithm("")

def animate_maze():
    global state, sorting_data
    if algorithms.get() == "Dijkstra" or algorithms.get() == "A*":
        reset("")
        border = main_board.create_border()

        maze = main_board.create_maze_board(2, main_board.rows - 3, 2, main_board.columns - 3, border)

        for node in maze:
            if node.state == "wall":
                canvas.create_rectangle(node.column * node_size,
                                        node.row * node_size,
                                        node.column * node_size + node_size,
                                        node.row * node_size + node_size,
                                        fill="grey", outline="black", tags="wall")
                canvas.update()
                time.sleep(0.001)

        state = "editable"
    else:
        canvas.delete("all")
        sorting_data = number_array = [i for i in range(200 - data_amount_slider.get() * 3, 0, -1)]
        draw_sorting_data(sorting_data)

def randomize_data():
    reset("")
    if algorithms.get() == "Dijkstra" or algorithms.get() == "A*":
        main_board.create_random_maze_board()
        draw_board(main_board)

selected_node = main_board.nodes[0][0]
def display_node_information(event):
    global element_information, selected_node
    try:
        canvas.create_rectangle(selected_node.column * node_size + 1, selected_node.row * node_size + 1,
                                selected_node.column * node_size + node_size - 1,
                                selected_node.row * node_size + node_size - 1, outline=color_dictionary[selected_node.state])
        current_row = math.floor(event.y / node_size)
        current_column = math.floor(event.x / node_size)

        selected_node = main_board.nodes[current_row][current_column]
        element_information.set("Node Information \nRow: " + str(selected_node.row) + "\nColumn: " + str(selected_node.column) + "\nDistance to start: " + str(selected_node.distance_to_start) +
                             "\nDistance to finish: " + str(selected_node.distance_to_finish) +
                             "\nAbsolute weight: " + str(selected_node.absolute_weight))
        canvas.create_rectangle(selected_node.column * node_size + 1, selected_node.row * node_size + 1, selected_node.column * node_size + node_size - 1,
                                selected_node.row * node_size + node_size - 1, outline="black")
    except:
        return

position = 1
def display_element_information(event):
    global element_information, position
    canvas.itemconfig(element_ids[int(position)], fill="black")

    tags_list = event.widget.itemcget(event.widget.find_withtag(CURRENT)[0], "tags").split()

    value = tags_list[1]
    position = sorting_data.index(int(value))
    element_information.set("Element Information \nPosition: " + str(position) + "\nValue: " + str(value))

    canvas.itemconfig(element_ids[int(position)], fill="grey")

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

canvas.grid(row=1, column=0, columnspan=12)


# top
top_row = tkinter.Frame(root)
top_row.grid(row=0, column=0, columnspan=12, sticky="N")

data_amount = tkinter.StringVar()
data_amount_label = tkinter.Label(top_row, textvariable=data_amount, font=("", 16))
data_amount_label.grid(row=0, column=0, sticky="S")
data_amount_slider = tkinter.Scale(top_row, from_=50, to=20, orient=tkinter.HORIZONTAL, length=200, showvalue=False, command=reset)
data_amount_slider.set(35)
data_amount_slider.grid(row=0, column=1, sticky="w")

reset_button = tkinter.Button(top_row, text="Reset", font=("", 14), bg="white", command=lambda: reset(""))
reset_button.grid(row=0, column=2, sticky="w", padx=10)

recursive_maze_and_worst_case = tkinter.Button(top_row, text="", font=("", 14), bg="white", command=lambda: animate_maze())
recursive_maze_and_worst_case.grid(row=0, column=4, sticky="w", padx=10)

randomize = tkinter.Button(top_row, text="", font=("", 14), bg="white", command=lambda: randomize_data())
randomize.grid(row=0, column=5, sticky="w", padx=10)


# left side
element_information = tkinter.StringVar()
element_information_label = Label(root, textvariable=element_information, bg="#D0D0D0", font=("Helvatical bold", 20), justify="left")
element_information_label.grid(row=2, column=0, rowspan=10, sticky=NW)


# middle
algorithm_information = tkinter.StringVar()
algorithm_information_label = Label(root, textvariable=algorithm_information, bg="#D0D0D0", font=("",14))
algorithm_information_label.grid(row=2, column=2, columnspan=5, pady=(0, 20))

start_algorithm = tkinter.Button(root, text="Algorithmus starten", font=("", 20), bg="#88ff88", command=lambda: animate_algorithm())
start_algorithm.grid(row=3, column=4)

show_information_text = tkinter.StringVar()
show_information_text.set("Nodeinformationen anzeigen")
set_show_information_button = tkinter.Button(root, textvariable=show_information_text, command=lambda: set_show_information())
#set_show_information_button.grid(row=3, column=14, padx=10, pady=10)

algorithms = StringVar(root)
algorithms.set("Quicksort") # default value
choose_algorithm = OptionMenu(root, algorithms, "Dijkstra", "A*", "Quicksort", command=select_algorithm)
choose_algorithm.config(font=("", 20), bg="white")
choose_algorithm.grid(row=4, column=4)


# right side
delay_information = tkinter.StringVar()
delay_label = Label(root, textvariable=delay_information, font=("", 14), bg="#D0D0D0")
delay_label.grid(row=2, column=10, sticky=N)

animation_speed_label = Label(root, text="Animation speed", font=("", 16 ))
animation_speed_label.grid(row=3, column=9, sticky=N)
animation_speed_slider = Scale(root, from_=50, to=1, orient=HORIZONTAL, command=update_delay, showvalue=False, length=200)
animation_speed_slider.set(25)
animation_speed_slider.grid(row=3, column=10, sticky=N)

skip_animation_button = tkinter.Button(root, text="Skip animation", font=("", 14), bg="white", command=lambda: skip_animation())
skip_animation_button.grid(row=4, column=10, sticky=N)


root.mainloop()