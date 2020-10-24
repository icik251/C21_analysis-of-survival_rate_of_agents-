import subprocess
import random
import time
import sys
import os
from classes.json_service import JsonService

SOURCE_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()

""" Set parameters values for the experiment. Default parameters are set but everything can be changed
    and parameters can be added. Check readme.md for detailed information about the parameters.
"""

json_dict['cover_radius'] = 100
json_dict['cost_value'] = 3
json_dict['random_seed'] = None
json_dict['to_cover'] = True
json_dict['dir_to_save_exp'] = "SingleExperiments\\"

json_service_obj.update_json_dict(json_dict)

# main_beta.py expects argument "exp_number" so that we can save multiple
# experiments results
exp_number = 1
subprocess.run(
    'python {} --exp_number {}'.format(os.path.join(SOURCE_FILE_DIR, "main.py"), exp_number),
    shell=True)
