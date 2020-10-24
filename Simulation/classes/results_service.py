import os

class ResultService:
    def __init__(self, config_dict, num_survived_agents, 
    exp_number=None, waves_of_bullets=None, 
    agents_to_wave=None, comp_time_to_wave=None):
        """Results Service 

            config_dict:
                The JSON configuration settings passed as python dictionary.
            num_survived_agents:
                Number of survived agents for the simulation.
            exp_number:
                Number of experiment. Used for creating the result file name, so if it's not passed
                no results are saved.
            waves_of_bullets:
                Waves of bullets fired for the simulation.
            agents_to_wave:
                Dictionary with key: simulation time step and value: alive agents
            comp_time_to_wave:
                Dictionary with key: time step and value: time taken for the simulation loop
        """

        self.exp_number = exp_number
        self.waves_of_bullets = waves_of_bullets
        self.agents_to_wave = agents_to_wave
        self.comp_time_to_wave = comp_time_to_wave
        self.config_dict = config_dict
        self.num_survived_agents = num_survived_agents
        
        if self.config_dict['dir_to_save_exp'] is not None:
            self.dir_name = os.path.join("Experiments", self.config_dict['dir_to_save_exp'])
        else:
            self.dir_name = None

        self.create_results_dir_if_not_exist()

    def is_exp_number_provided(self):
        """
        This method checks if self.exp_number is provided.
        """
        if self.exp_number is None:
            return False
        else:
            return True

    def create_results_dir_if_not_exist(self):
        """
        Create directory to save experiments if it doesn't exist.
        """
        if self.dir_name is not None:
            if not os.path.exists(self.dir_name):
                os.makedirs(self.dir_name)

    def save_results(self):
        """
        Saving results in a text file in the provided directory.
        """

        if not self.is_exp_number_provided():
            return 1
        else:
            text_file = open(os.path.join(self.dir_name, 
                                "exp_{}_random_seed_{}.txt".format(self.exp_number, self.config_dict['random_seed'])), "w")
            text_file.write(
            "Number of Initial Agents: %s \nNumber of Agents survived: %s \nNumber of wave of bullets fired: %s \n" %
            (self.config_dict['wave_length'], self.num_survived_agents, self.waves_of_bullets))
            text_file.write("\n")
            text_file.write("Variables Used \n")
            text_file.write(
            "Agent Velocity: %s\n" %
            (self.config_dict['agent_vel'] *
            self.config_dict['sim_speed']))
            text_file.write(
            "Bullet Velocity: %s\n" %
            (self.config_dict['bullet_vel'] *
            self.config_dict['sim_speed']))
            text_file.write("Number of Agents: %s\n" % self.config_dict['wave_length'])
            text_file.write("Number of Waves: %s\n" % self.config_dict['no_of_waves'])
            text_file.write("Covering Radius: %s\n" % self.config_dict['cover_radius'])
            text_file.write("Agent covering (Boolean): %s\n" % self.config_dict['to_cover'])
            text_file.write("Cost Function Value: %s\n" % self.config_dict['cost_value'])
            text_file.write("Config Dictionary for Graph: %s\n" % self.agents_to_wave)
            text_file.write("Config Dictionary for Comp Time: %s\n" % self.comp_time_to_wave)
            text_file.close()
            return 0