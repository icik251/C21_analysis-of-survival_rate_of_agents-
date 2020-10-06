import config
import random
from main_beta import main
import time

list_of_cost_values = list(range(1,6))
list_of_waves = list(range(1,5))
list_of_agents = list(range(10,50,5))
# For running multiple experiments
# Changing radius from 50 to 200 with step 10
main_param = 'cover_radius'
for i in range(50, 200, 10):
    param_value = str(i)
    config.cover_radius = i
    print(config.cover_radius)
    for j in range(100):
        config.cost_value = random.choice(list_of_cost_values)
        config.no_of_waves = random.choice(list_of_waves)
        config.wave_length = random.choice(list_of_agents)
        main(main_parameter=main_param, parameter_value=param_value, exp_number=j)
        time.sleep(5)