# Requirements
Install python version 3.8.5

Use the following code in the command prompt:
pip install -r requirements.txt

# How to run experiments
Change the following parameters for the simulation in config.txt. The file is in JSON format, values can be changed automatically and saved in the file.
* sim_speed : The speed of the simulation. The default value is 1. The parameter can take any positive integer.
* agent_vel : Velocity of the agents, which has a default and recommended value of 1.5. The default value is chosen by empirically, while trying to make the simulation realistic as possible.
* bullet_vel : Velocity of the bullets, which has a default and recommended value of 7. The default value is chosen by empirically, while trying to make the simulation realistic as possible.
* wave_length : Number of initialized agents in a wave. The default value is 30 and we do not plan to change the value for the experiments. The parameter can take any positive integer.
* cover_radius : The radius of communication, which limits the scope of the agents while protecting other agents. The default value is 100. We plan to do experiments with the default value and 200. The parameter can take any positive integer.
* no_of_waves: Waves of agents that are going to be initialized. The default value is 1. The parameter can take any positive integer. 
* to_cover : Boolean variable that defines if agents should cover or not. The default value is True, however for our baseline experiments we will change it to False.
* show_covering : Boolean variable to toggle to see the radius of communication of each agent. The default value is False. The parameter is created only with visualization purpose.
* random_seed : This parameter helps us to replicate experiments if that is needed. The default value is None. The parameter can take any integer. Drones and missiles are going to be spawned at the same coordinates every simulation for the same integer.
* dir_to_save_exp : Directory where the current experiment is saved. The default value is None. The parameter can take any string that is a directory path.
* cost_value : Number of times each agent can cover other agents. The default value is 3, however we plan to do experiments with values of 1 and 2 as well. The parameter can take any positive integer.

Parameter to implement:
* communication - The type of communication for the current simulation. The default value is None. The parameter can take string values "decentralized" or "centralized" for decentralized or centralized communication, respectively.

The result text file is saved in the directory provided from parameter "dir_to_save_exp". You can observe the following results for the values of variables:

1. Outputs: 
* Number of Initial Agents 
* Number of Agents survived
* Number of wave of bullets fired

2. Variables:
* Agent Velocity
* Bullet Velocity
* Number of Agents
* Number of Waves
* Covering Radius
* Agent covering (Boolean)
* Cost Function Value
* Config Dictionary for Graph