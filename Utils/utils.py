import numpy as np, copy, os
from matplotlib import pyplot as plt 

color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_blue = (0, 0, 255)
color_purple = (128, 0, 128)

def maze_to_img(m, size):
    a =[[color_black if m[y][x][0] == "#" else color_white if m[y][x][0] == "." else color_blue if m[y][x][0] == "*" else color_purple if m[y][x][0] == "O" else "?" for x in range(size)]for y in range(size)]      
    plt.imshow(a)
    plt.show()

def save_file(maze, size):
    repo = os.path.abspath(os.path.join(__file__ ,"../../_output"))
    if not os.path.exists(repo):
        os.makedirs(repo)
    file_name = input("\nInput - Name of the saved file: ")+".txt"
    with open(repo+"/"+file_name, 'w') as output:
        for nrow in range(size):
            line = ""
            for ncol in range(size):
                line += maze[nrow][ncol][0]
            line += "\n"
            output.write(line)

def read_file():
    fname = input("Name of the file to solve: ")
    repo = os.path.abspath(os.path.join(__file__ ,"../../_output/"+fname+".txt"))
    with open(repo, "r") as f:
        contenu = f.read().splitlines()
    size = len(contenu[0])
    maze = [[[contenu[y][x], False] for x in range(size)] for y in range(size)]
    return maze, size

def print_maze(maze, size):
    for y in range(size):
        line = ""
        for x in range(size):
            line += maze[y][x][0]
        print(line)