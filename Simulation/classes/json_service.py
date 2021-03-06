import os
import json


class JsonService:
    def __init__(self):
        """ Service for JSON processing.

            When an object is initialized, if the 'config.json' doesn't exist,
            it is created automatically with the default parameter values.
        """

        if not self.json_config_exists():
            self.json_dict = dict()
            # Simulation speed
            self.json_dict['sim_speed'] = 1
            # RECOMMENDED VALUE = "1.5". Velocity of the agents moving up to
            # the finish line.
            self.json_dict['agent_vel'] = 1.5 * self.json_dict['sim_speed']
            # RECOMMENDED VALUE = "7". Velocity of the bullets firing down onto
            # the agents.
            self.json_dict['bullet_vel'] = 7 * self.json_dict['sim_speed']
            # Number of agents present in one wave.
            self.json_dict['wave_length'] = 30
            # Radius each agent covers to shield other agents. Variable value
            # is in Pixels.
            self.json_dict['cover_radius'] = 100
            # Waves of agents that will try to reach the finish line.
            self.json_dict['no_of_waves'] = 1
            # Boolean Variable to change if agents will cover each other or
            # not.
            self.json_dict['to_cover'] = True
            # Boolean Variable to toggle to see the covering radius of each
            # agent.
            self.json_dict['show_covering'] = True
            # Number of times each agent can cover other agents. "0" means no agent
            # covers and "99" means agent covers as many times as possible.
            self.json_dict['cost_value'] = 3
            # random seed value
            self.json_dict['random_seed'] = None
            # directory to save experiment into
            self.json_dict['dir_to_save_exp'] = None
            # changing between communication approaches
            self.json_dict['communication'] = 'baseline'

            self.save_json()

    def save_json(self):
        """
            Save JSON file.
        """
        with open('config.json', 'w') as json_file:
            json.dump(self.json_dict, json_file)

    def read_json(self):
        """
            Read JSON file.
        """
        with open('config.json') as json_file:
            self.json_dict = json.load(json_file)

    def get_json_dict(self):
        """
            Return a python dictionary with the JSON data.
        """
        self.read_json()
        return self.json_dict

    def update_json_dict(self, new_dict):
        """
            Save a new dictionary as JSON file.
        """
        self.json_dict = new_dict
        self.update_communication()
        self.save_json()

    def json_config_exists(self):
        """
            Check if JSON file exists.
        """
        if os.path.isfile('config.json'):
            return True
        else:
            return False
        
    def update_communication(self):
        """ 
            Set show_covering and to_cover to False if communication is None
        """
        if self.json_dict['communication'] == 'baseline':
            self.json_dict['show_covering'] = False
            self.json_dict['to_cover'] = False
        elif self.json_dict['communication'] == 'centralized' or self.json_dict['communication'] == 'decentralized':
            self.json_dict['to_cover'] = True