# DFS Generator:
# Backtrack, recursion

from random import randrange
import sys, time, numpy as np

utils = "\\".join(sys.path[0].split("\\")[:-1]) + "\\Utils" 
sys.path.append(utils)

import utils

n = int(input("Input the size of the maze (nb. of different way from the main one): "))  # nombre de couloir depuis le chemin entrée -> sortie
size = (n * 2) + 1
maze = [["." if y%2==1 and x%2==1 else "#" for y in range(size)] for x in range(size)]
board = [[[False, False, False, False] for y in range(n)] for x in range(n)] # top, left, bot, right
new_objs = []

def print_maze():
    for y in range(size):
        line = ""
        for x in range(size):
            line += maze[y][x]
        print(line)

def translate_maze():
    for y in range(1, size, 2):
        for x in range(1, size, 2):
            posY = int(y/2)
            posX = int(x/2)
            maze[y-1][x] = "." if board[posY][posX][0] else "#"
            maze[y][x-1] = "." if board[posY][posX][1] else "#"
            maze[y+1][x] = "." if board[posY][posX][2] else "#"
            maze[y][x+1] = "." if board[posY][posX][3] else "#"

# Retourne les cases voisines valides à partir d'une position
# Valide si visite est FALSE et si la case est entourée de mur, autrement pas valide
def get_objs(y, x):
    new_objs.clear()
    for i,wall in enumerate(board[y][x]):
        if board[y][x][i]:
            continue
        else:
            if y == 0 and i == 0 or x == 0 and i == 1 or y == n-1 and i == 2 or x == n-1 and i == 3:
                new_objs.append([[(y,x), i], [(y,x), i]])
                continue
            if i == 0 and not is_looping(y-1,x):
                new_objs.append([[(y,x), 0],[(y-1,x), 2]]) # [[pos, wall],[target_pos, target_wall]]
            elif i == 1 and not is_looping(y,x-1):    
                new_objs.append([[(y,x), 1], [(y,x-1), 3]])
            elif i == 2 and not is_looping(y+1,x):
                new_objs.append([[(y,x), 2], [(y+1,x), 0]])
            elif i == 3 and not is_looping(y,x+1):
                new_objs.append([[(y,x), 3], [(y,x+1), 1]])
            
    if len(new_objs) > 1:
        np.random.shuffle(new_objs)
        return new_objs
    elif len(new_objs) == 1:
        return new_objs
    return None

def is_looping(y, x):
    if board[y][x][0] != False:
        return True
    if board[y][x][1] != False:
        return True
    if board[y][x][2] != False:
        return True
    if board[y][x][3] != False:
        return True
    return False

def DFS():
    objets = [[[(0, 0), 0],[(0, 0), 0]]]
    while len(objets) > 0:
        obj = objets.pop(-1)
        pos = obj[0][0]
        target_pos = obj[1][0]
        if is_looping(target_pos[0], target_pos[1]):
            continue
        source_id = obj[0][1]
        target_id = obj[1][1]

        board[pos[0]][pos[1]][source_id] = True
        board[target_pos[0]][target_pos[1]][target_id] = True

        news_objs = get_objs(target_pos[0], target_pos[1]) 
        if news_objs != None:    
            for i,new_obj in enumerate(news_objs):
                objets.append(new_obj)

def maze_manager():
    s = time.time()
    DFS()
    translate_maze()
    set_matrice()
    
    #utils.print_maze()
    print("\nGeneration completed in:", round(time.time()-s, 3), "sec.")

    utils.maze_to_img(maze, size)
    utils.save_file(maze, size)

# crée l'entrée du maze en détruisant 2x # (dont un de maniere aléatoire)
# crée la sortie vers le bas droite
def set_matrice():
    x = randrange(2)
    if x == 1:
        maze[-1][-2]="."# en bas a gauche
    else:
        maze[-2][-1]="." # en bas a droite

    maze[0][0]="."
    maze[-1][-1]="."
    if maze[-2][-2] == False:
        for i in range(3, 10):
            if x == 1: # bloc en bas à gauche détruit
                if maze[-2][-i] == ".":
                    for y in range(size-i, size):
                        maze[-1][y] = "."
                    break
            else: # bloc en bas à droite détruit
                if maze[-i][-2] == ".":
                    for y in range(size-i, size):
                        maze[y][-1] = "."
                    break

maze_manager()