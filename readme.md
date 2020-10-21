# Requirements
Install Python 3.8.5.

Use the following line in the command prompt to install all dependencies:
pip install -r requirements.txt

# Parameters
Parameter values are saved in "config.json" which is created automatically if it does not exist while trying to run a simulation. On the first creation of the file, the parameters are set with the default values. The parameters can be changed by using the class "JsonService" in "json_service.py". 

How to use JsonService?
1. Initialize object of the class.
2. Call method get_json_dict(), which returns the content of the json as dictionary.
3. Change parameters in dictionary. Example: 
json_dict['cover_radius'] = 100
json_dict['cost_value'] = 3
json_dict['random_seed'] = None
json_dict['to_cover'] = True
4. Call method update_json_dict(new_dict), where "new_dict" expects a dictionary (the json_dict with the changed parameter values). This method will save the new config.json file.
5. Run simulation (see the next section). 

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

# How to run a single experiment
1. Make sure to set parameter values (see the section above). Otherwise the experiment is going to be conducted with the default values. You can do that in the "single_experiment.py" file.
2. Run "single_experiment.py" file.

# How to run multiple experiments (our experiment design)
1. Make sure to set parameter values (see the section above). Otherwise the experiment is going to be conducted with the default values. You can do that in the "multiple_experiment.py" file. 
2. Run "multiple_experiment.py" file.

If you want to replicate experimental results use parameter "random_seed".

# Results output
The result text file is saved in the directory provided from parameter "dir_to_save_exp". You can observe the following results:

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
* Dictionary for Computation Time
