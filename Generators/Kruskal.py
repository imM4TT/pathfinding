# Kruskal Maze gen:
# 1/ Set uniq ID for each cell
# 2/ Set list of every edge connexion possible
# 3/ Connect random edge
# 4/ Merge ID

from random import randrange
import sys, time, numpy as np

utils = "\\".join(sys.path[0].split("\\")[:-1]) + "\\Utils" 
sys.path.append(utils)

import utils

n = int(input("Input the size of the maze (nb. of different way from the main one): "))  
size = (n * 2) + 1

## maze[y][x][0/1] valeur/id
maze = []

edges = [[],[],[],[]]

## liste qui contient tous les id avec leurs positions
id = []
NESW = [(-1, 0), (0, 1), (1, 0), (0, -1)]

## utilisé pour connecter 2
def connect(edge):
    source_id = maze[edge[0][0]][edge[0][1]][1]
    target_id = maze[edge[2][0]][edge[2][1]][1]

    if is_looping(source_id, target_id):
        return None, 0, 0, 0

    wall_id = maze[edge[1][0]][edge[1][1]][1]
    wall_pos = (edge[1][0], edge[1][1])
    return wall_pos, wall_id, source_id, target_id      
        
# permet un merge des cellules sur les id correspondant
def merge_id(source_id, wall_id, target_id):
    y, x = id[wall_id][1][0] # récupere la position du mur pour pouvoir changer son id
    maze[y][x][1] = source_id # nouvelle attribution d'id pour le mur
    id[source_id][1].append((y, x)) # ajout de sa position dans l'id correspondant
    for pos in id[target_id][1]:
        id[source_id][1].append(pos)
        maze[pos[0]][pos[1]][1] = source_id

def is_looping(source_id, target_id):
    return source_id == target_id

idx = 0
# return a random edge
def get_edge():
    if len(edges[0]):
        return edges[0].pop(0)
    
    if len(edges[1]):
        return edges[1].pop(0)
    
    if len(edges[2]):
        return edges[2].pop(0)

    return edges[3].pop(0)

def Kruskal():
    global total_empty    
    walls_down = 0
    while walls_down < total_empty-1:
        edge = get_edge() # Pull out initial empty
        wall_pos, wall_id, source_id, target_id = connect(edge) # get wall to destroy & IDs to merge
        if wall_pos != None:
            merge_id(source_id, wall_id, target_id) # Merge
            maze[wall_pos[0]][wall_pos[1]][0] = "." # Wall down
            walls_down += 1

# Drivers code
def maze_manager():
    s = time.time()
    start() 
    print("\nInitialization:", round(time.time()-s, 3), "sec.")
    Kruskal()
    set_matrice()
    #utils.print_maze()
    print("\nGeneration completed in:", round(time.time()-s, 3), "sec.")
    utils.maze_to_img(maze, size)
    utils.save_file(maze, size)


total_empty = 0
def start():
    global total_empty
    c = -1
    for y in range(size):
        maze.append([])
        for x in range(size):
            maze[y].append([])
            if x==0 or x==size-1 or y==0 or y==size-1:
                maze[y][x] = "#"
            else:
                c += 1
                if x%2==1 and y%2==1:
                    maze[y][x] = [".", c]
                    total_empty += 1
                    np.random.shuffle(NESW)
                    for i, dir in enumerate(NESW):
                        empty_pos = (y+dir[0]*2, x+dir[1]*2)
                        wall_pos = (y+dir[0], x+dir[1])
                        if empty_pos[0] < 1 or empty_pos[0] > size-2 or empty_pos[1] < 1 or empty_pos[1] > size-2:
                            continue
                        edges[i].append([(y, x), (wall_pos[0], wall_pos[1]), (empty_pos[0], empty_pos[1])])

                else:
                    maze[y][x] = ["#", c]
                id.append([c, [(y, x)]])
    np.random.shuffle(edges[0])
    np.random.shuffle(edges[1])
    np.random.shuffle(edges[2])
    np.random.shuffle(edges[3])
    np.random.shuffle(edges)

# crée l'entrée du maze en détruisant 2x # (dont un de maniere aléatoire)
# crée la sortie vers le bas droite
def set_matrice():
    x = randrange(2)
    if x == 1:
        maze[0][1]="."
        maze[-1][-2]="."# en bas a gauche
    else:
        maze[1][0]="."
        maze[-2][-1]="." # en bas a droite

    maze[0][0]="."
    maze[-1][-1]="."
    if maze[-2][-2][0] == "#":
        for i in range(3, 10):
            if x == 1: # bloc en bas à gauche détruit
                if maze[-2][-i][0] == ".":
                    for y in range(size-i, size):
                        maze[-1][y] = "."
                    break
            else: # bloc en bas à droite détruit
                if maze[-i][-2][0] == ".":
                    for y in range(size-i, size):
                        maze[y][-1] = "."
                    break

maze_manager()