import random

def collide(obj1, obj2):
    """ Collide function is used to check for pixel perfect collisions using masks.
        Mask is used to check for pixel perfect collisions.

        obj1/obj2:
            Objects to check if the collide. Must have mask property.
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))


def move_agents(agents, survived_agents, agent_vel):
    """ This method moves the agents.

        agents:
            List of agents in the environment.
        survived_agents:
            Count of survived agents.
        agent_vel:
            Velocity of agents.
    """
    # Loop to update position of every agent every frame (To make them move up)
    for agent in agents[:]:
        # Move agent up with the velocity defined
        agent.move(agent_vel)
        # A statement to see if the Agent crosses the line(which is y = 0),
        # then
        if agent.y < 150:
            # increase the count of agents survived
            survived_agents += 1
            # And remove the agent from the list of agents as it is now
            # offscreen
            agents.remove(agent)
    return survived_agents


def cover(obj1, obj2):
    """ This method is for covering.

        obj1/obj2:
            Object covers another object.
    """
    if not obj1.cover:
        obj2.x = obj1.x
        obj2.y = obj1.y
        obj2.y -= 80

def centralized_logic(agents, xxpos, config_dict, bool_loc, bool_config, bool_perm_config, bool_move):
        cover_counter = 0
        cover_list = []
        global_cover_list = []
        agent_counter = 0
        boundary_int = 3000
        permut_list = []
        new_global_perms = []
        global_perms = []
        x = 0
        # This part finds every possible location a drone can go as long as it doesnt conside with another drone
        if(bool_loc == True):
            for agent in agents[:]:
                for tnega in agents:
                    for k in range(-2,2):
                        for l in range(-2,2):
                            if abs(agent.x - tnega.x) + k* xxpos < config_dict['cover_radius'] and abs(agent.y - tnega.y) + l* xxpos < config_dict['cover_radius']:# checks the possible directions of movement in terms of the location of the drones that can be covered
                                if tnega.y + l*xxpos > agent.y:# aviods drones to move backwards
                                    cover_list.append([tnega.x + k*xxpos,tnega.y + l*xxpos])# logs the possible movement directions in terms of the covered drones directions
                global_cover_list.append(cover_list)# creates a list of possible movement locations for every drone
                cover_list =[]
            bool_loc = False
            
        # This part calculates possible drone configurations
        if (bool_config == True):
            while x < boundary_int:# the numer of configuration permutations
                for i in range(len(global_cover_list)):
                    r = random.randrange(0,len(global_cover_list[i]))# randomly pick from the configuration
                    permut_list.append(global_cover_list[i][r])# add to a local list
                global_perms.append(permut_list)# add to a global list 
                permut_list = []
                x += 1
        
        bool_config = False
        perm_counter = 0
        general_perm_counter = 0
        # calculates the possible permutations of configuration and finds the one that lines up the most drones in all x directions
        if bool_perm_config == True:
            for i in range(len(global_perms)):
                for j in range(len(global_perms[i])):
                    for k in range(len(global_perms[i])):
                        if global_perms[i][j][0] == global_perms[i][k][0] :# if the x values are the same, increase the counter
                            if j != k:# avoids comparing drones against itself
                                perm_counter += 1
                if perm_counter > general_perm_counter:# keep a general counter
                    general_perm_counter = perm_counter# always take the highest value
                    #print(general_perm_counter)
                    perm_counter = 0

                    best_list = global_perms[i]# get the configuration that has the highest x direction linings
        bool_perm_config = False
        
        agent_count = 0

        #moves the drones to the points that has been calculated above 
        if bool_move == True:  
            for agent in agents[:]:
                agent.x = best_list[agent_count][0]# moves the x direction
                agent.y = best_list[agent_count][1]# moves the y direction
                agent_count += 1
        bool_move = False
        
        return agents, bool_loc, bool_config, bool_perm_config, bool_move