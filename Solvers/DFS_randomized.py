# DFS Solver randomized variant:
# Backtrack, recursion

import sys, time, numpy as np

utils = "\\".join(sys.path[0].split("\\")[:-1]) + "\\Utils" 
sys.path.append(utils)

import utils

maze = []
size = 0

# Retourne les cases voisines valides à partir d'une position
# Valide si visite est FALSE et si la case est entourée de mur, autrement pas valide
def get_valid_pos(y, x):
    directions = []
    # BAS
    if y < size - 1:
        if maze[y+1][x][0] == "." and maze[y+1][x][0] != "O":
            directions.append((y+1, x))       
    # DROITE                                  
    if x < size - 1:                          
        if maze[y][x+1][0] == "." and maze[y][x+1][0] != "O":
            directions.append((y, x+1))        
    # HAUT                                     
    if y > 1:                                  
        if maze[y-1][x][0] == "." and maze[y-1][x][0] != "O":# pour pouvoir aller en haut il faut etre sur la ligne 2 au minimum
            directions.append((y-1, x))        
    # GAUCHE                                   
    if x > 1:                                  
        if maze[y][x-1][0] == "." and maze[y][x-1][0] != "O":
            directions.append((y, x-1))
    
    if len(directions):
        np.random.shuffle(directions)
        return directions[0]
    return None

def DFS():
    positions = [(0, 0)]
    nb = 0
    while len(positions) > 0:
        nb += 1
        y = positions[-1][0] # on selectionne la derniere ligne valide
        x = positions[-1][1] # on selectionne la derniere colonne valide
        maze[y][x][0] = "O"
        new_pos = get_valid_pos(y, x) # on récupère une cellules voisine valide
        if new_pos != None:           # que l'on sauvegarde dans notre liste target
            if new_pos == (size-1, size-1):
                maze[-1][-1][0] = "O"
                return True, nb
            positions.append(new_pos)
        else:
            maze[y][x][0] = "*"
            del positions[-1]
    return False, 0

def maze_manager():
    global maze, size
    maze, size = utils.read_file()
    s = time.time()
    solved, nb, = DFS()
    #utils.print_maze()
    print("\nSolved in", nb, "steps,", round(time.time()-s, 3), "sec." if solved else "Non solved")
    utils.maze_to_img(maze, size)
    utils.save_file(maze, size)


maze_manager()