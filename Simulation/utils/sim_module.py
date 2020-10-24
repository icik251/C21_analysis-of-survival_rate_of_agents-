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
