The requirements:
1. Install python version 3.8.5

2.install requirements:
Use the following code in the command prompt:
pip install -r requirements.txt

3. Change the following parameters for the simulation in config.py
-- sim_speed : the speed of the simulation, the default value is 3
-- agent_vel : the velocity of the agents, default value set to 1.5 times the simulation speed. It is not recommended to change this value. 
-- bullet_vel : the velocity of the bullets the default value is 7 times the simulation speed. Change this value to simulate different firing rates
-- wave_length : Number of agents present in one wave. The fault value is 30. Change this value to simulate different agent amounts.
-- cover_radius : Radius each agent covers to shield other agents. Variable value is in Pixels. The fault value is 30. Change this value to simulate different decentralized information exchange rates.
-- no_of_waves: Waves of agents that will try to reach the finish line.The defualt value is 1. Change this to simulate how many lines of drones will enter the line of fire. 
-- To_cover : Boolean Variable to change if agents will cover each other or not. The default value is True
-- Show_covering : Boolean Variable to toggle to see the covering radius of each agent.The default value is True
-- cost_value : Number of times each agent can cover other agents. "0" means no agent covers and "99" means agent covers as many times as possible. The default value is 3. Change this to limit the movement of the covering drones

4. The results: 
open the file Results.txt

You can observe the following results for the values of variables:

-- Outputs: 
Number of Initial Agents 
Number of Agents survived
Number of wave of bullets fired

-- Variables:
Agent Velocity
Bullet Velocity
Number of Agents
Number of Waves
Covering Radius
Agent covering (Boolean)
Cost Function Value

5. To Do
Experiments to run:
-- Change of all parameters and compare them with the number of agents survive such as:
a. How the survival rate of agents changes with different values for cover radius. This is going to explain how the surviving rate is effected under different rates of decentralized and centralized communication. When the cover_radius is infinity, the system has central communication.
b. Compare the collective survival rate for consecutive waves of drones. This will help us understand for what agent_vel', bullet_vel and wave_length values the primary wave can fully or partially protect the secondary wave.
c. Compare the wave_length with respect to cover_radius to compare how the amount of information available changes the survival rates for the different number of drones.
d. How the survival rates of agents change in terms of the cost function. This will help us understand how immobility of the drones affect the survival rates.







