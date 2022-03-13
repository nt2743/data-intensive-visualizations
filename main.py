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

canvas = Canvas(root, width=1000, height=500)

main_board = Board(20, 40)

node_information = ""

#represents the current program state
state = "editable"

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
                    color = "green"
                case "wall":
                    color = "grey"

            canvas.create_rectangle(column * 25, row * 25, column * 25 + 25, row * 25 + 25,
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
    canvas.create_rectangle(math.floor(event.x / 25) * 25, math.floor(event.y / 25) * 25,
                            math.floor(event.x / 25) * 25 + 25, math.floor(event.y / 25) * 25 + 25,
                            fill="grey", outline="black", tags="wall")
    main_board.nodes[math.floor(event.y / 25)][math.floor(event.x / 25)].state = "wall"

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
    canvas.create_rectangle(math.floor(event.x / 25) * 25, math.floor(event.y / 25) * 25,
                            math.floor(event.x / 25) * 25 + 25, math.floor(event.y / 25) * 25 + 25,
                            fill="white", outline="black", tags="node")
    main_board.nodes[math.floor(event.y / 25)][math.floor(event.x / 25)].state = "node"

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
    if main_board.nodes[math.floor(event.y / 25)][math.floor(event.x / 25)].state != "node":
        return

    new_row = math.floor(event.y / 25)
    new_column = math.floor(event.x / 25)
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
        color = "green"
        distance = math.inf
    canvas.create_rectangle(previous_column * 25, previous_row * 25,
                            previous_column * 25 + 25, previous_row * 25 + 25,
                            fill="white", outline="black", tags="node")
    main_board.nodes[previous_row][previous_column].state = "node"
    main_board.nodes[previous_row][previous_column].distance_to_start = math.inf

    canvas.create_rectangle(new_column * 25, new_row * 25,
                            new_column * 25 + 25, new_row * 25 + 25,
                            fill=color, outline="black", tags=start_or_end)
    main_board.nodes[new_row][new_column].state = start_or_end
    main_board.nodes[new_row][new_column].distance_to_start = distance

def is_in_start(x, y):
    if main_board.start_row * 25 <= y < main_board.start_row * 25 + 25 and main_board.start_column * 25 <= x < main_board.start_column * 25 + 25:
        return True
    return False

def is_in_finish(x, y):
    if main_board.finish_row * 25 <= y < main_board.finish_row * 25 + 25 and main_board.finish_column * 25 <= x < main_board.finish_column * 25 + 25:
        return True
    return False

def animate (board, animation_type):
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

def visualize(board, nodes_in_order, color, node_state):
    global state
    state = "visualizing"
    node = nodes_in_order.pop(0)
    if node.state == node_state:
        canvas.create_rectangle(node.column * 25, node.row * 25, node.column * 25 + 25, node.row * 25 + 25, fill=color, outline="black", tags=node_state)
    if len(nodes_in_order) > 0:
        root.after(animation_speed_slider.get(), visualize, board, nodes_in_order, color, node_state)
    else:
        if color == "cyan":
            visualize(board, shortest_path(board), "yellow", "node")
        if color == "yellow":
            state = "visualized"

def reset_board(board):
    global main_board
    canvas.delete("all")
    main_board = Board(20,40)
    draw_board(main_board)

def create_random_maze():
    reset_board(main_board)
    main_board.create_random_maze_board()
    draw_board(main_board)

def skip_animation():
    animation_speed_slider.set(0)

def display_node_information(event):
    global node_information
    current_row = math.floor(event.y / 25)
    current_column = math.floor(event.x / 25)
    node = main_board.nodes[current_row][current_column]
    node_information = "row: " + str(node.row) + " column: " + str(node.column) + " distance_to_start: " + str(node.distance_to_start) + " distance_to_finish: " + str(node.distance_to_finish)
    print(node_information)


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

node_information_label = Label(root, text=node_information)
node_information_label.pack()

start_algorithm = tkinter.Button(root, text="Algorithmus starten", command=lambda: animate(main_board, algorithms.get()))
start_algorithm.pack()

algorithms = StringVar(root)
algorithms.set("Dijkstra") # default value

choose_algorithm = OptionMenu(root, algorithms, "Dijkstra", "A*")
choose_algorithm.pack()

clear_board = tkinter.Button(root, text="Zurücksetzen", command=lambda: reset_board(main_board))
clear_board.pack()

clear_paths = tkinter.Button(root, text="Wege entfernen", command=lambda: draw_board(main_board))
clear_paths.pack()

maze = tkinter.Button(root, text="Labyrinth erzeugen", command=lambda: animate(main_board, "recursive division maze"))
maze.pack()

random_maze = tkinter.Button(root, text="Zufälliges Labyrinth erzeugen", command=lambda: create_random_maze())
random_maze.pack()

draw_bord = tkinter.Button(root, text="Board zeichnen", command=lambda: draw_board(main_board))
draw_bord.pack()

animation_speed_label = Label(root, text="Geschwindigkeit der Animation")
animation_speed_label.pack()
animation_speed_slider = Scale(root, from_=0, to=20, orient=HORIZONTAL)
animation_speed_slider.set(10)
animation_speed_slider.pack()

skip_animation_button = tkinter.Button(root, text="Animation überspringen", command=lambda: skip_animation())
skip_animation_button.pack()

root.mainloop()