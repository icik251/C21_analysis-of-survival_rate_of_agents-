from json_service import JsonService
import random
import main_beta
import time
import subprocess

list_of_cost_values = list(range(1,6))
list_of_waves = list(range(1,5))
list_of_agents = list(range(10,50,5))

json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()


# For running multiple experiments
# Changing radius from 50 to 200 with step 10
main_param = 'cover_radius'
for i in range(50, 200, 10):
    param_value = i
    json_dict['cover_radius'] = i
    for j in range(100):
        json_dict['cost_value'] = random.choice(list_of_cost_values)
        json_dict['no_of_waves'] = random.choice(list_of_waves)
        json_dict['wave_length'] = random.choice(list_of_agents)
        # update changes in json
        json_service_obj.update_json_dict(json_dict)

        subprocess.run('python Pygame_Simulation\\main_beta.py --main_parameter {} --parameter_value {} --exp_number {}'.format(main_param, json_dict['cover_radius'], j), shell=True)
        #time.sleep(8)