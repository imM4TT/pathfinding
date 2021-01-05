# AStar solver 2.0, avec implémentation d'un DFS pour pondérer uniquement aux intersections
# Pathfinder basé sur le poids total du noeud suivant (F):
# F = G + H | Plus le F est petit plus le noeud est à favorisé car il est considéré comme étant le plus proche de la sortie
# G = distance entre la position du noeud courant et la position de départ
# H = distance estimée entre la position du noeud courant et la position de fin

import sys, time, numpy as np

utils = "\\".join(sys.path[0].split("\\")[:-1]) + "\\Utils" 
sys.path.append(utils)

import utils

maze = []
size = 0
cardinals_dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
nb_step = 0

class Node:
    
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0
        self.child = []

    def set_value(self,h):
        self.f = self.g+h
        self.h = h

def is_solved(current_node):
    if current_node.position == (size-1, size-1): # le noeud courant est localisé en position d'arrivée
        path = []                                 # on récupère/retourne tous ses noeuds parents, ce qui correspond au chemin de sortie
        current = current_node
        while current:
            path.append(current.position)
            current = current.parent
        return path
    return None

def DFS_get_next_nodes(current_node):
    global nb_step
    next_nodes = [] # liste des prochains nodes à retourner
    positions = [] # positions pour le dfs
    finding_next_node = get_valids_pos(current_node.position[0], current_node.position[1])

    for i, pos in enumerate(finding_next_node): # a partir du noeud courant, on cherche et renvoie tous les autres noeuds
        positions.append(pos)

    parent = current_node
    local_g = 0
    
    while len(positions):
        #print("position", pos, nb_step)
        nb_step += 1
        local_g += 1
        y, x = positions.pop(-1)
        
        #print("finding", finding_next_node)
        if is_a_node(y, x):
            new_node = Node((y,x), parent)
            new_node.g = local_g
            next_nodes.append(new_node)
            parent = current_node
            local_g = 0
        else:
            n = Node((y,x), parent)
            parent = n
            finding_next_node = get_valids_pos(y, x)
            if finding_next_node != None:
                positions.append(finding_next_node[0])
            else:
                parent = current_node
                local_g = 0
        maze[y][x][0] = "*"
    return next_nodes

def is_a_node(y, x):
    nb_empty = 0
    for dir in cardinals_dir:
        new_pos = (y+dir[0], x+dir[1])
        if new_pos[0] > size-1 or new_pos[0] < 0 or new_pos[1] > size-1 or new_pos[1] < 0: # on vérifie qu'on soit dans le labyrinthe
            continue
        if maze[new_pos[0]][new_pos[1]][0] == "." or maze[new_pos[0]][new_pos[1]][0] == "*":
            nb_empty += 1
    return nb_empty > 2 or (y, x) == (size-1, size-1)

def get_valids_pos(y, x):
    valids_pos = []
    for dir in cardinals_dir:
        new_pos = (y+dir[0], x+dir[1])
        if new_pos[0] > size-1 or new_pos[0] < 0 or new_pos[1] > size-1 or new_pos[1] < 0: # on vérifie qu'on soit dans le labyrinthe
            continue
        elif maze[new_pos[0]][new_pos[1]][0] == "#": # on vérifie qu'on est sur un "."
            continue
        elif maze[new_pos[0]][new_pos[1]][1]: # on vérifie que le noeud ne fait pas parti du chemin existant
            continue

        maze[y][x][1] = True # cellule visité
        valids_pos.append(new_pos)

    if len(valids_pos):
        return valids_pos
    return None

def AStar():
    startNode = Node((0,0))
    endNode = Node((size-1,size-1))
    nodes = [startNode] # contient tous les noeuds à explorer

    while len(nodes):
        current_node = sorted(nodes, key=lambda x:x.f)[0]
        del nodes[nodes.index(current_node)]
        solved = is_solved(current_node)
        if solved:
            return solved
        #print("\ncurrent position:", current_node.position)
        #list(map(lambda x:print("Nodes: ",x.position), nodes))

        next_nodes = DFS_get_next_nodes(current_node)
        for next_node in next_nodes: # assignation des valeurs f g h
            #print("noeuds suivants: ", next_node.position, " poids:", next_node.g)
            h = abs(endNode.position[0]-next_node.position[0]) + abs(endNode.position[1]-next_node.position[1])
            next_node.set_value(h)
            nodes.append(next_node)
    return "Unsolved"

def maze_manager():
    global maze, size
    maze, size = utils.read_file()
    s = time.time()

    path = AStar()
  
    set_path(path)
    #utils.print_maze()

    print("Solved in", nb_step, "steps,", round(time.time()-s, 3), "sec." if len(path) else print("Unsolved"))
    utils.maze_to_img(maze, size)
    utils.save_file(maze, size)

def set_path(path):
    for i, position in enumerate(path):
        maze[position[0]][position[1]][0] = "O"

maze_manager()
