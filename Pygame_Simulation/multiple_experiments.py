from json_service import JsonService
import random
import main_beta
import time
import subprocess

list_of_cost_values = list(range(1,4))
#list_of_agents = list(range(25,35))
list_of_agents = [30]
list_of_cover_radius = [100, 200]
json_service_obj = JsonService()
json_dict = json_service_obj.get_json_dict()

json_dict['to_cover'] = True

#json_dict['random_seed'] = 3
num_of_experiments = 100
# For running multiple experiments
for cover_radius_val in list_of_cover_radius:
    json_dict['cover_radius'] = cover_radius_val
    for cost_value in list_of_cost_values:
        json_dict['cost_value'] = cost_value
        for agents_num in list_of_agents:
            json_dict['wave_length'] = agents_num
            for i in range(num_of_experiments):

                # set the directory to save
                json_dict['dir_to_save_exp'] = 'cover_radius_{}\\cost_value_{}\\wave_length_{}\\'.format(cover_radius_val,
                cost_value, agents_num)

                # update changes in json
                json_service_obj.update_json_dict(json_dict)

                subprocess.run('python Pygame_Simulation\\main_beta.py --exp_number {}'.format(i), shell=True)