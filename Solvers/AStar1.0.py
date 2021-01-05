# AStar solver
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

class Node:
    
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def set_value(self, g, h):
        self.f = g+h
        self.g = g 
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

def get_next_nodes(current_node):
    y, x = current_node.position
    nodes = []
    for dir in cardinals_dir:
        new_pos = (y+dir[0], x+dir[1])
        if new_pos[0] > size-1 or new_pos[0] < 0 or new_pos[1] > size-1 or new_pos[1] < 0: # on vérifie qu'on soit dans le labyrinthe
            continue
        elif maze[new_pos[0]][new_pos[1]][0] == "#": # on vérifie qu'on dans sur un "."
            continue
        elif maze[new_pos[0]][new_pos[1]][1]: # on vérifie que le noeud ne fait pas parti du chemin existant
            continue

        nodes.append(Node(new_pos, current_node))

    return nodes

# Driver code
def AStar():
    startNode = Node((0,0))
    endNode = Node((size-1,size-1))
    nodes = [startNode] # contient tous les noeuds à explorer
    nb_step = 0
    while len(nodes):
        current_node = sorted(nodes, key=lambda x:x.f)[0]                    # trie tous les noeuds non explorés selon le plus petit indice F
        maze[current_node.position[0]][current_node.position[1]][1] = True   # définit le noeud comme étant visité
        del nodes[nodes.index(current_node)]                                 # supprime le noeud courant de la liste

        solved = is_solved(current_node)                                     # condition d'arrêt, vraie lorsque le maze est résolu
        if solved:
            return solved, nb_step

        next_nodes = get_next_nodes(current_node)  # récupère tous les noeuds suivant à partir d'un noeud parent

        for next_node in next_nodes:               # assignation des valeurs f g h
            g = current_node.g + 1
            h = abs(endNode.position[0]-next_node.position[0]) + abs(endNode.position[1]-next_node.position[1])
            next_node.set_value(g, h)

            nodes.append(next_node)
        maze[current_node.position[0]][current_node.position[1]][0] = "*"
        nb_step += 1

def maze_manager():
    global maze, size
    maze, size = utils.read_file()
    s = time.time()

    path, nb_step = AStar()

    set_path(path)
    #utils.print_maze()

    print("Solved in", nb_step, "steps,", round(time.time()-s, 3), "sec." if len(path) else print("Unsolved"))
    utils.maze_to_img(maze, size)
    utils.save_file(maze, size)

def set_path(path):
    for i, position in enumerate(path):
        maze[position[0]][position[1]][0] = "O"


maze_manager()