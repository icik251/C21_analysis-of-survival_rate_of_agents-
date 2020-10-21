import subprocess
import main_beta
import random
import time
import sys
import os
from json_service import JsonService

json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()

"""Set parameters values for the experiment. Default parameters are set but everything can be changed
and parameters can be added. Check readme.md for detailed information about the parameters."""

json_dict['cover_radius'] = 100
json_dict['cost_value'] = 3
json_dict['random_seed'] = None
json_dict['to_cover'] = True
json_dict['dir_to_save_exp'] = "SingleExperiments\\"

json_service_obj.update_json_dict(json_dict)

# main_beta.py expects argument "exp_number" so that we can save multiple experiments results
subprocess.run(
    'python Pygame_Simulation\\main_beta.py --exp_number {}'.format(1),
    shell=True)
