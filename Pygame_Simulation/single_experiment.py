import subprocess
import main_beta
import random 
import time 
import sys 
from json_service import JsonService

list_of_cost_values = list(range(1,6))
list_of_agents = list(range(10,50,5))

json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()


json_dict['cover_radius'] = 50
json_dict['cost_value'] = random.choice(list_of_cost_values)
json_dict['wave_length'] = random.choice(list_of_agents)

json_service_obj.update_json_dict(json_dict)

main_aparam = 'single_exp_cov_radius'
subprocess.run('python Pygame_Simulation\\main_beta.py --main_parameter {} --parameter_value {} --exp_number {}'.
format(main_aparam, 50, 1), shell=True)