import random
import time, sys, os

"""
    n = rows
    m = columns
"""
n = 10
m = 10
game_grid = []
dict_of_missiles = dict()
dict_of_drones = dict()
    
def create_game_grid():
    for i in range(n):
        game_grid.append([' '] * m)


def update_dict(object_id, coordinates, keyword=''):
    """
    object_id - unique object number
    coordinates - x,y tuple
    keyword - string from which we know which dict to update
    """
    if keyword == 'drones':
        dict_of_drones[object_id] = coordinates
    elif keyword == 'missiles':
        dict_of_missiles[object_id] = coordinates

def populate_drones():
    drone_id = 0
    for i in range(n-3,n):
        for j in range(2):
            rand_num = random.randint(0,n-1)
            while game_grid[i][rand_num]=='D':
                rand_num = random.randint(0,n-1)
            game_grid[i][rand_num]='D'
            update_dict(drone_id, (rand_num,i), keyword='drones')
            drone_id+=1

def populate_missiles():
    missile_id = 0
    for i in range(0,2):
        for j in range(2):
            rand_num = random.randint(0,n-1)
            while game_grid[i][rand_num]=='|':
                rand_num = random.randint(0,n-1)
            game_grid[i][rand_num]='|'
            update_dict(missile_id, (rand_num,i), keyword='missiles')
            missile_id+=1

def print_grid():
    for index, row in enumerate(game_grid):
        print(index, *row, sep=' ')
    print(' ', *list(range(0, m)), sep=' ')
    time.sleep(1)
    sys.stdout.flush()
    #print('-----------------------')

def is_move_in_grid(coordinates, keyword=''):
    if keyword == 'drones':
        if coordinates[1] == 0:
            return False
        else:
            return True
    elif keyword == 'missiles':
        if coordinates[1] == 9:
            return False
        else:
            return True

def missiles_move():
    "reversed iteration because otherwise a missile ovewrites another one"
    for missile_id, coordinates in reversed(dict_of_missiles.items()):
        if is_move_in_grid(coordinates, keyword='missiles'):
            new_y = coordinates[1]+1
            "update game grid, delete old position, place new one"
            game_grid[coordinates[1]][coordinates[0]] = ' '
            game_grid[new_y][coordinates[0]] = '|'
            "update dictionary"
            dict_of_missiles[missile_id] = (coordinates[0], new_y)
    

def drones_move():
    for drone_id, coordinates in dict_of_drones.items():
        if is_move_in_grid(coordinates, keyword='drones'):
            new_y = coordinates[1]-1
            "update game grid, delete old position, place new one"
            game_grid[coordinates[1]][coordinates[0]] = ' '
            game_grid[new_y][coordinates[0]] = 'D'
            "update dictionary"
            dict_of_drones[drone_id] = (coordinates[0], new_y)

def next_frame():
    drones_move()
    missiles_move()

def run_game(frames=10):
    create_game_grid()
    populate_drones()
    populate_missiles()
    for i in range(frames):
        #print(dict_of_missiles)
        #print(dict_of_drones)
        print_grid()
        next_frame()
        print('-----------------------')

run_game()