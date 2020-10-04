# Simulation speed
sim_speed = 1
# RECOMMENDED VALUE = "1.5". Velocity of the agents moving up to the finish line.
agent_vel = 1.5 * sim_speed
# RECOMMENDED VALUE = "7". Velocity of the bullets firing down onto the agents.
bullet_vel = 7 * sim_speed
wave_length = 30  # Number of agents present in one wave.
# Radius each agent covers to shield other agents. Variable value is in Pixels.
cover_radius = 100
no_of_waves = 1  # Waves of agents that will try to reach the finish line.
# Boolean Variable to change if agents will cover each other or not.
To_cover = True
# Boolean Variable to toggle to see the covering radius of each agent.
Show_covering = True
# Number of times each agent can cover other agents. "0" means no agent
# covers and "99" means agent covers as many times as possible.
cost_value = 3