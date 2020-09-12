import random
import time, sys, os
from collections import defaultdict

"""
    n = rows
    m = columns
"""
n = 10
m = 10

lifes = 3
game_grid = []

dict_of_missiles = dict()
dict_of_drones = dict()
dict_of_next_movements = dict()
dict_of_drones_scope = dict()
dict_of_lifes = dict()

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
        dict_of_lifes[object_id] = lifes
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

def is_move_in_grid_missiles(coordinates):
    if coordinates[1] == 9:
        return False
    else:
        return True

def drone_possible_moves_in_grid(coordinates):
    list_of_possible_moves = []
    for x in range(-1,2):
        for y in range(-1,2):
            if coordinates[0] + x >= 0:
                list_of_possible_moves.append((coordinates[0] + x, y))
            if coordinates[1] + y <= m or coordinates[1] + y >= 0: 
                list_of_possible_moves.append((x, coordinates[1]+y))

    return list_of_possible_moves


def missiles_move():
    "reversed iteration because otherwise a missile ovewrites another one"
    for missile_id, coordinates in reversed(list(dict_of_missiles.items())):
        if is_move_in_grid_missiles(coordinates):
            new_y = coordinates[1]+1
            "update game grid, delete old position, place new one"
            game_grid[coordinates[1]][coordinates[0]] = ' '
            game_grid[new_y][coordinates[0]] = '|'
            "update dictionary"
            dict_of_missiles[missile_id] = (coordinates[0], new_y)
    

def drones_move():
    for drone_id, coordinates in dict_of_drones.items():
        list_of_possible_moves = drone_possible_moves_in_grid(coordinates)
        print('Possible moves for drone at: {}'.format(coordinates))
        print(list_of_possible_moves)
            
            
        new_y = coordinates[1]-1
        "update game grid, delete old position, place new one"
        game_grid[coordinates[1]][coordinates[0]] = ' '
        game_grid[new_y][coordinates[0]] = 'D'
        "update dictionary"
        dict_of_drones[drone_id] = (coordinates[0], new_y)

def calculate_movement(drone_id):
    curr_min = 3
    curr_min_drone_id = None
    for drone_in_scope in dict_of_drones_scope[drone_id]:
        if curr_min > dict_of_lifes[drone_in_scope]:
            curr_min = dict_of_lifes[drone_in_scope]
            curr_min_drone_id = drone_in_scope


def move_forward(drone_id):
    coordinates = dict_of_drones[drone_id]
    if is_move_in_grid(coordinates, keyword='drones'):
        new_y = coordinates[1]-1
        dict_of_next_movements[drone_id] = (coordinates[0], new_y)
    else:
        cross_finish_line(drone_id)

def move_diagonal(drone_id):
    coordinates = dict_of_drones[drone_id]



def next_frame():
    drones_scope()
    drones_move()
    drone_got_hit()
    missiles_move()
    drone_got_hit()

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
        
def drone_got_hit():
    for drone_id, coordinates_d in dict_of_drones.items():
        for missile_id, coordinates_m in reversed(list(dict_of_missiles.items())):
            if coordinates_d == coordinates_m:
                "update dictionary"
                dict_of_lifes[drone_id] =  dict_of_lifes[drone_id] -1

def drones_scope():
        for drone_id_0, coordinates_d_s_0 in dict_of_drones.items():
            for drone_id_1, coordinates_d_s_1 in dict_of_drones.items():
                for i in range(-1,2):
                    for j in range(-1,2):
                        if drone_id_0 != drone_id_1:
                            if coordinates_d_s_0[0] + i  ==  coordinates_d_s_1[0]:
                                if coordinates_d_s_0[1] + j ==  coordinates_d_s_1[1]:
                                    print('Drone at: {} can see drone at {}'.format(dict_of_drones[drone_id_1], dict_of_drones[drone_id_0]))
                                    if drone_id_0 not in dict_of_drones_scope:
                                        dict_of_drones_scope[drone_id_0] = [drone_id_1]
                                    else:
                                        dict_of_drones_scope[drone_id_0].append(drone_id_1)

run_game()