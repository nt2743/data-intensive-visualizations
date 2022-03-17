import math
from Board import Board
import tkinter
from tkinter import *
from algorithms.Dijkstra import dijkstra, shortest_path
from algorithms.AStar import a_star
from mazes import Recursive_division

root = tkinter.Tk()
root.title("Pathfinding Visualization")
root.geometry("1000x800")

root.state("zoomed")

node_size = 25
canvas_height = 500
canvas_width = 1530
canvas = Canvas(root, height=canvas_height, width=canvas_width)
board_height = math.floor(canvas_height/node_size)
board_width = math.floor(canvas_width/node_size)

main_board = Board(board_height, board_width)

#represents the current program state
state = "editable"

step = 0 #for debugging

green = "#7CFC00"

def draw_board(board):
    for row in range(len(board.nodes)):
        for column in range(len(board.nodes[0])):
            node_state = board.nodes[row][column].state
            color = None
            match node_state:
                case "node":
                    color = "white"
                case "start":
                    color = "red"
                case "finish":
                    color = green
                case "wall":
                    color = "grey"

            canvas.create_rectangle(column * node_size, row * node_size, column * node_size + node_size, row * node_size + node_size,
                                            fill=color, outline="black", tags=node_state)

draw_board(main_board)

mouseClicked = False
# build walls
def begin_walls(event):
    global mouseClicked
    mouseClicked = True
    if not (is_in_start(event.x, event.y) or is_in_finish(event.x, event.y)) and state == "editable":
        mark_as_wall(event)

def build_walls(event):
    global mouseClicked
    if mouseClicked and not (is_in_start(event.x, event.y) or is_in_finish(event.x, event.y)) and state == "editable":
        mark_as_wall(event)

def complete_walls(event):
    global mouseClicked
    mouseClicked = False

def mark_as_wall(event):
    canvas.create_rectangle(math.floor(event.x / node_size) * node_size, math.floor(event.y / node_size) * node_size,
                            math.floor(event.x / node_size) * node_size + node_size, math.floor(event.y / node_size) * node_size + node_size,
                            fill="grey", outline="black", tags="wall")
    try:
        main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)].state = "wall"
    except:
        return

# delete walls
def begin_delete_walls(event):
    global mouseClicked
    mouseClicked = True
    if not (is_in_start(event.x, event.y) or is_in_finish(event.x, event.y)) and state == "editable":
        mark_as_node(event)

def delete_walls(event):
    global mouseClicked
    if mouseClicked and not (is_in_start(event.x, event.y) or is_in_finish(event.x, event.y)) and state == "editable":
        mark_as_node(event)

def complete_delete_walls(event):
    global mouseClicked
    mouseClicked = False

def mark_as_node(event):
    canvas.create_rectangle(math.floor(event.x / node_size) * node_size, math.floor(event.y / node_size) * node_size,
                            math.floor(event.x / node_size) * node_size + node_size, math.floor(event.y / node_size) * node_size + node_size,
                            fill="white", outline="black", tags="node")
    main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)].state = "node"

# move start and end
def pick(event):
    global mouseClicked
    mouseClicked = True

def drag_start(event):
    global mouseClicked
    if mouseClicked and not is_in_start(event.x, event.y) and state != "visualizing":
        mark_as_new_start_or_end(event, "start")

def drag_finish(event):
    global mouseClicked
    if mouseClicked and not is_in_finish(event.x, event.y) and state != "visualizing":
        mark_as_new_start_or_end(event, "finish")

def drop(event):
    global mouseClicked
    mouseClicked = False
    if state == "visualized":
        main_board.reset_after_algorithm()
        draw_board(main_board)
        animate(main_board, "dijkstra")

def mark_as_new_start_or_end(event, start_or_end):
    if main_board.nodes[math.floor(event.y / node_size)][math.floor(event.x / node_size)].state != "node":
        return

    new_row = math.floor(event.y / node_size)
    new_column = math.floor(event.x / node_size)
    if start_or_end == "start":
        previous_row = main_board.start_row
        previous_column = main_board.start_column
        main_board.start_row = new_row
        main_board.start_column = new_column
        color = "red"
        distance = 0
    else:
        previous_row = main_board.finish_row
        previous_column = main_board.finish_column
        main_board.finish_row = new_row
        main_board.finish_column = new_column
        color = green
        distance = math.inf
    canvas.create_rectangle(previous_column * node_size, previous_row * node_size,
                            previous_column * node_size + node_size, previous_row * node_size + node_size,
                            fill="white", outline="black", tags="node")
    main_board.nodes[previous_row][previous_column].state = "node"
    main_board.nodes[previous_row][previous_column].distance_to_start = math.inf

    canvas.create_rectangle(new_column * node_size, new_row * node_size,
                            new_column * node_size + node_size, new_row * node_size + node_size,
                            fill=color, outline="black", tags=start_or_end)
    main_board.nodes[new_row][new_column].state = start_or_end
    main_board.nodes[new_row][new_column].distance_to_start = distance

def is_in_start(x, y):
    if main_board.start_row * node_size <= y < main_board.start_row * node_size + node_size and main_board.start_column * node_size <= x < main_board.start_column * node_size + node_size:
        return True
    return False

def is_in_finish(x, y):
    if main_board.finish_row * node_size <= y < main_board.finish_row * node_size + node_size and main_board.finish_column * node_size <= x < main_board.finish_column * node_size + node_size:
        return True
    return False

def animate (board, animation_type):
    global state
    if animation_type == "Dijkstra":
        draw_board(board)
        main_board.reset_after_algorithm()
        visualize(board, dijkstra(main_board), "cyan", "node")
        state = "visualized"
    if animation_type == "A*":
        draw_board(board)
        main_board.reset_after_algorithm()
        visualize(board, a_star(main_board, state, step), "cyan", "node")
        #state = "visualized"
    if animation_type == "recursive division maze":
        reset_board(board)
        border = main_board.create_border()
        visualize(board, Recursive_division.create_maze_board(main_board, 2, main_board.rows - 3, 2, main_board.columns - 3, border), "grey", "wall")
        state = "editable"

def visualize(board, nodes_in_order, color, node_state):
    node = nodes_in_order.pop(0)
    if node.state == node_state:
        canvas.create_rectangle(node.column * node_size, node.row * node_size, node.column * node_size + node_size, node.row * node_size + node_size, fill=color, outline="black", tags=node_state)
    if len(nodes_in_order) > 0:
        if state == "debugging":
            speed = 0
        else:
            speed = animation_speed_slider.get()
        root.after(speed, visualize, board, nodes_in_order, color, node_state)
    else:
        if color == "cyan":
            nodes_shortest_path = shortest_path(board)
            path_length.set("Weglänge: " + str(len(nodes_shortest_path)))
            visualize(board, nodes_shortest_path, "yellow", "node")

def animate_step_by_step (board, animation_type):
    if animation_type == "Dijkstra":
        draw_board(board)
        main_board.reset_after_algorithm()
        visualize(board, dijkstra(main_board), "cyan", "node")
    if animation_type == "A*":
        draw_board(board)
        main_board.reset_after_algorithm()
        visualize(board, a_star(main_board), "cyan", "node")
    if animation_type == "recursive division maze":
        reset_board(board)
        border = main_board.create_border()
        visualize(board, Recursive_division.create_maze_board(main_board, 2, main_board.rows - 3, 2, main_board.columns - 3, border), "grey", "wall")

def visualize_step_by_step(board, nodes_in_order, color, node_state):
    global state
    state = "visualizing"
    node = nodes_in_order.pop(0)
    if node.state == node_state:
        canvas.create_rectangle(node.column * node_size, node.row * node_size, node.column * node_size + node_size, node.row * node_size + node_size, fill=color, outline="black", tags=node_state)
    if len(nodes_in_order) > 0:
        root.after(animation_speed_slider.get(), visualize, board, nodes_in_order, color, node_state)
    else:
        if color == "cyan":
            visualize_step_by_step(board, shortest_path(board), "yellow", "node")
        if color == "yellow":
            state = "visualized"

def start_debugging():
    global state, debug_button_text, step
    if state == "debugging":
        debug_button_text.set("Debugging starten")
        state = "editable"
    else:
        step = 0
        debug_button_text.set("Debugging beenden")
        state = "debugging"

def step_forward():
    global step
    step += 1
    animate(main_board, algorithms.get())

def reset_board(board):
    global main_board, board_height, board_width
    canvas.delete("all")
    board_height = math.floor(canvas_height / node_size)
    board_width = math.floor(canvas_width / node_size)
    main_board = Board(board_height,board_width)
    draw_board(main_board)

def create_random_maze():
    reset_board(main_board)
    main_board.create_random_maze_board()
    draw_board(main_board)

def skip_animation():
    animation_speed_slider.set(0)

def display_node_information(event):
    global node_information
    try:
        current_row = math.floor(event.y / node_size)
        current_column = math.floor(event.x / node_size)
        node = main_board.nodes[current_row][current_column]
        node_information.set("Row: " + str(node.row) + "\nColumn: " + str(node.column) + "\nDistance to start: " + str(node.distance_to_start) + "\nDistance to finish: " + str(round(node.distance_to_finish,2)))
    except:
        return

def set_node_size(event):
    global node_size
    node_size = node_size_slider.get()
    reset_board(main_board)
    draw_board(main_board)


canvas.tag_bind("node", "<Button-1>", begin_walls)
canvas.tag_bind("node", "<Motion>", build_walls)
canvas.tag_bind("node", "<ButtonRelease-1>", complete_walls)

canvas.tag_bind("wall", "<Button-1>", begin_delete_walls)
canvas.tag_bind("wall", "<Motion>", delete_walls)
canvas.tag_bind("wall", "<ButtonRelease-1>", complete_delete_walls)

canvas.tag_bind("start", "<Button-1>", pick)
canvas.tag_bind("start", "<Motion>", drag_start)
canvas.tag_bind("start", "<ButtonRelease-1>", drop)

canvas.tag_bind("finish", "<Button-1>", pick)
canvas.tag_bind("finish", "<Motion>", drag_finish)
canvas.tag_bind("finish", "<ButtonRelease-1>", drop)

canvas.tag_bind("node" or "start" or "finish" or "", "<Enter>", display_node_information)
canvas.pack()

node_information = tkinter.StringVar()
node_information.set("Row: \nColumn:\n Distance to start:\n Distance to finish: ")
node_information_label = Label(root, textvariable=node_information, bg="#D0D0D0", font=("Helvatical bold",20), justify="left")
node_information_label.pack(side="left")

start_algorithm = tkinter.Button(root, text="Algorithmus starten", command=lambda: animate(main_board, algorithms.get()))
start_algorithm.pack()

debug_button_text = tkinter.StringVar()
debug_button_text.set("Debugging starten")
start_algorithm_step_by_step = tkinter.Button(root, textvariable=debug_button_text, command=lambda: start_debugging())
start_algorithm_step_by_step.pack()

step_forward_button = tkinter.Button(root, text="Schritt weiter", command=lambda: step_forward())
step_forward_button.pack()

algorithms = StringVar(root)
algorithms.set("Dijkstra") # default value

choose_algorithm = OptionMenu(root, algorithms, "Dijkstra", "A*")
choose_algorithm.pack()

path_length = tkinter.StringVar()
path_length.set("")
path_length_label = Label(root, textvariable=path_length)
path_length_label.pack()

node_size_label = Label(root, text="Größe der Nodes")
node_size_label.pack(side="right")
node_size_slider = Scale(root, from_=10, to=50, orient=HORIZONTAL, command=set_node_size)
node_size_slider.set(node_size)
node_size_slider.pack(side="right")

clear_board = tkinter.Button(root, text="Zurücksetzen", command=lambda: reset_board(main_board))
clear_board.pack(side="right")

clear_paths = tkinter.Button(root, text="Wege entfernen", command=lambda: draw_board(main_board))
clear_paths.pack(side="right")

maze = tkinter.Button(root, text="Labyrinth erzeugen", command=lambda: animate(main_board, "recursive division maze"))
maze.pack(side="right")

random_maze = tkinter.Button(root, text="Zufälliges Labyrinth erzeugen", command=lambda: create_random_maze())
random_maze.pack(side="right")

draw_bord = tkinter.Button(root, text="Board zeichnen", command=lambda: draw_board(main_board))
draw_bord.pack(side="right")

animation_speed_label = Label(root, text="Geschwindigkeit der Animation")
animation_speed_label.pack()
animation_speed_slider = Scale(root, from_=1, to=50, orient=HORIZONTAL)
animation_speed_slider.set(10)
animation_speed_slider.pack()

skip_animation_button = tkinter.Button(root, text="Animation überspringen", command=lambda: skip_animation())
skip_animation_button.pack()

root.mainloop()