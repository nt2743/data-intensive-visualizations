import math
from Board import Board
import tkinter
from tkinter import *
from algorithms.Dijkstra import dijkstra, shortest_path
from mazes import Recursive_division

root = tkinter.Tk()
root.title("Pathfinding Visualization")
root.geometry("1000x700")

canvas = Canvas(root, width=1000, height=500)

main_board = Board(20, 40)

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
                    color = "black"

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
                            fill="black", outline="black", tags="wall")
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
    if mouseClicked and not is_in_start(event.x, event.y) and state == "editable":
        mark_as_new_start_or_end(event, "start")

def drag_finish(event):
    global mouseClicked
    if mouseClicked and not is_in_finish(event.x, event.y) and state == "editable":
        mark_as_new_start_or_end(event, "finish")

def drop(event):
    global mouseClicked
    mouseClicked = False

def mark_as_new_start_or_end(event, start_or_end):
    if main_board.nodes[math.floor(event.y / 25)][math.floor(event.x / 25)].state != "node":
        return

    new_row = math.floor(event.y / 25)
    new_column = math.floor(event.x / 25)
    if start_or_end == "start":
        previous_row = main_board.startRow
        previous_column = main_board.startColumn
        main_board.startRow = new_row
        main_board.startColumn = new_column
        color = "red"
        distance = 0
    else:
        previous_row = main_board.finishRow
        previous_column = main_board.finishColumn
        main_board.finishRow = new_row
        main_board.finishColumn = new_column
        color = "green"
        distance = math.inf
    canvas.create_rectangle(previous_column * 25, previous_row * 25,
                            previous_column * 25 + 25, previous_row * 25 + 25,
                            fill="white", outline="black", tags="node")
    main_board.nodes[previous_row][previous_column].state = "node"
    main_board.nodes[previous_row][previous_column].distance = math.inf

    canvas.create_rectangle(new_column * 25, new_row * 25,
                            new_column * 25 + 25, new_row * 25 + 25,
                            fill=color, outline="black", tags=start_or_end)
    main_board.nodes[new_row][new_column].state = start_or_end
    main_board.nodes[new_row][new_column].distance = distance

def is_in_start(x, y):
    if main_board.startRow * 25 <= y < main_board.startRow * 25 + 25 and main_board.startColumn * 25 <= x < main_board.startColumn * 25 + 25:
        return True
    return False

def is_in_finish(x, y):
    if main_board.finishRow * 25 <= y < main_board.finishRow * 25 + 25 and main_board.finishColumn * 25 <= x < main_board.finishColumn * 25 + 25:
        return True
    return False

#TODO: name = "animate" to make it work for algorithms and mazes
def visualize (board, nodes_in_order):
    draw_board(board)
    visualize_dijkstra(board, nodes_in_order)

def visualize_dijkstra(board, nodes_in_order):
    global state
    state = "visualizing"
    node = nodes_in_order.pop(0)
    if node.state == "node":
        canvas.create_rectangle(node.column * 25, node.row * 25, node.column * 25 + 25, node.row * 25 + 25, fill="cyan", outline="black", tags="node")
    if len(nodes_in_order) > 0:
        root.after(10,visualize_dijkstra, board, nodes_in_order)
    else:
        visualize_shortest_path(board, shortest_path(board))

def visualize_shortest_path(board, nodes_shortest_path):
    global state
    node = nodes_shortest_path.pop(0)
    if node.state == "node":
        canvas.create_rectangle(node.column * 25, node.row * 25, node.column * 25 + 25, node.row * 25 + 25, fill="yellow",
                            outline="black", tags="visualized")
    if len(nodes_shortest_path) > 0:
        root.after(10,visualize_shortest_path, board, nodes_shortest_path)
    else:
        state = "editable"

def reset_board(board):
    global main_board
    canvas.delete("all")
    main_board = Board(20,40)
    draw_board(main_board)

def visualize_maze(board, created_maze):
     #draw_board(board)
     create_maze(board, created_maze)

def create_maze(board, created_maze):
    node = created_maze.pop(0)
    if node.state == "wall":
        canvas.create_rectangle(node.column * 25, node.row * 25, node.column * 25 + 25, node.row * 25 + 25, fill="black",
                                outline="black", tags="wall")
    if len(created_maze) > 0:
        root.after(20, create_maze, board, created_maze)

def create_random_maze():
    reset_board(main_board)
    main_board.create_random_maze_board()
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

canvas.pack()

startAlgorithm = tkinter.Button(root, text="Algorithmus starten", command=lambda: visualize(main_board, dijkstra(main_board)))
startAlgorithm.pack()

clear_board = tkinter.Button(root, text="Zurücksetzen", command=lambda: reset_board(main_board))
clear_board.pack()

clear_paths = tkinter.Button(root, text="Wege entfernen", command=lambda: draw_board(main_board))
clear_paths.pack()

maze = tkinter.Button(root, text="Labyrinth erzeugen", command=lambda: visualize_maze(main_board, Recursive_division.create_maze_board(main_board, 0, main_board.rows, 0, main_board.columns)))
maze.pack()

random_maze = tkinter.Button(root, text="Zufälliges Labyrinth erzeugen", command=lambda: create_random_maze())
random_maze.pack()

draw_bord = tkinter.Button(root, text="Board zeichnen", command=lambda: draw_board(main_board))
draw_bord.pack()

root.mainloop()