import subprocess
import random
import time
import sys
import os
from classes.json_service import JsonService
import main

SOURCE_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()

""" 
    Set parameters values for the experiment. Default parameters are set but everything can be changed
    and parameters can be added. Check readme.md for detailed information about the parameters.
"""

json_dict['cover_radius'] = 100
json_dict['cost_value'] = 2
json_dict['random_seed'] = 5
json_dict['communication'] = 'centralized'
json_dict['dir_to_save_exp'] = "SingleExperiments"

json_service_obj.update_json_dict(json_dict)

# logic() expects argument "exp_number" so that we can save multiple
# experiments results
exp_number = 11
for i in range(10):
    main.logic(exp_number)