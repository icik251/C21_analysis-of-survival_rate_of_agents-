import random
import time
import subprocess
import os
from classes.json_service import JsonService

SOURCE_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()

""" Set parameters values for the multiple experiments. The set values are corresponding
    to our experiment design. Check readme.md for detailed information about the parameters.
"""

json_dict['to_cover'] = True
list_of_cost_values = list(range(1, 4))
list_of_agents = [30]
list_of_cover_radius = [100, 200]

# Number of experiments per configuration
num_of_experiments = 1

# For running multiple experiments
for cover_radius_val in list_of_cover_radius:
    json_dict['cover_radius'] = cover_radius_val
    for cost_value in list_of_cost_values:
        json_dict['cost_value'] = cost_value
        for agents_num in list_of_agents:
            json_dict['wave_length'] = agents_num
            for i in range(num_of_experiments):

                # set the directory to save experiment
                json_dict['dir_to_save_exp'] = 'cover_radius_{}\\cost_value_{}\\wave_length_{}\\'.format(
                    cover_radius_val, cost_value, agents_num)

                # update changes in json
                json_service_obj.update_json_dict(json_dict)

                # main_beta.py expects argument "exp_number" so that we can save multiple experiments results
                subprocess.run(
                    'python {} --exp_number {}'.format(os.path.join(SOURCE_FILE_DIR,"main.py"), i),
                    shell=True)
