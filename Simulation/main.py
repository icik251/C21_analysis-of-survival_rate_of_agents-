import pygame
import os
import time
import random
import sys
import warnings
from datetime import datetime

from classes.json_service import JsonService
from classes.agent import Agent
from classes.bullet import Bullet
from classes.results_service import ResultService
from utils.sim_module import *


def logic(exp_number=None):
    """ Main logic of the simulation.
        Here, initialization and movement of agents is happening.

        exp_number:
            An integer that will be used for the name of the text file for the results. If it's set to None,
            results text file is not going to be created.
    """
    
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    """Set PyGame settings"""

    # To show counter, font needs to be initialized
    pygame.font.init()
    # Set window width/height and name of window
    WIDTH, HEIGHT = 1000, 800
    # The main window to show the running simulation
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Agent Simulation")
    # Using the font to display surviving agents
    main_font = pygame.font.SysFont("comicsans", int(WIDTH / 25))

    """Load everything needed for the simulation"""
    # Load JSON file
    json_service_obj = JsonService()
    CONFIG_DICT = json_service_obj.get_json_dict()
    print(CONFIG_DICT)
    random.seed(CONFIG_DICT['random_seed'])
    
    # Get directory of current file
    SOURCE_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(SOURCE_FILE_DIR)
    # Load assets
    ASSETS_DIR = os.path.join(SOURCE_FILE_DIR, "assets")
    # Drone
    RED_AGENT = pygame.transform.scale(pygame.image.load(
    os.path.join(ASSETS_DIR, "pixel_ship_red_small.png")), (40, 30))
    # Lasers
    RED_LASER = pygame.transform.scale(pygame.image.load(
    os.path.join(ASSETS_DIR, "pixel_laser_red.png")), (50, 40))
    # Backgrond
    BG = pygame.transform.scale(
    pygame.image.load(
        os.path.join(
            ASSETS_DIR,
            "background-black.png")),
    (WIDTH,
     HEIGHT))

    waves_of_bullets = 0
    tick_counter = 0
    agents_to_wave = dict()
    comp_time_to_wave = dict()
    ms1 = int(round(time.time() * 1000))
    run = True  # To make the main loop run
    FPS = 120  # Pygame FPS
    survived_agents = 0  # Count the number of agents surviving
    agents = []  # List to store all the agents on screen
    bullets = []  # List to store all the bullets on the screen
    # An object to help track time, will be used to run pygame on specific FPS
    clock = pygame.time.Clock()
    bullet_time = 500 / CONFIG_DICT['sim_speed']  # milisecond
    xpos = 40
    xxpos = int((WIDTH - xpos * 2) / (CONFIG_DICT['wave_length'] - 1))
    number_waves = CONFIG_DICT['no_of_waves']
    just_once = False
    
    bool_loc, bool_config, bool_perm_config, bool_move = True, True, True, True

    def redraw_window():
        """ This function can only be called in "main" Function. Basically updates window every frame
            blit draws the image on the background at the given coordinates.
        """

        WIN.blit(BG, (0, 0))

        # Drawing counter on the screen
        counter_label = main_font.render(
            f"Agents Survived: {survived_agents}", 1, (255, 255, 255))
        WIN.blit(counter_label, (10, 10))
        pygame.draw.line(WIN, (255, 0, 0), (0, 150), (WIDTH, 150), 2)

        for agent in agents:
            # Every screen update, draw the agents present in the agents[] list
            # on the screen
            agent.draw(WIN)
        for bullet in bullets:
            # Every screen update, draw the bullets present in the bullets[]
            # list on screen
            bullet.draw(WIN)

        # Updates the entire surface/screen every loop
        pygame.display.update()

    while run:
        # Means that for every second at most "FPS" frames should pass. Here,
        clock.tick(FPS)

        start_while_time = datetime.now()
        agents_to_wave[tick_counter] = survived_agents + len(agents)
        tick_counter += 1
        xpos = 40  # x-Position of the initial agent. Hard coded.

        # Logic states, If there is no agent on the screen and the required
        # number of waves have not gone already, send in the next wave
        if len(agents) == 0 and number_waves > 0:
            # initialising to run the loop "length" number of times to create
            # the required number of agents
            for i in range(CONFIG_DICT['wave_length']):
                agent = Agent(x=xpos, y=random.randrange(HEIGHT - 100, HEIGHT),
                              config_dict=CONFIG_DICT, ship_img=RED_AGENT)
                # Add the new initialized agent to the agent list
                agents.append(agent)
                xpos += xxpos  # Incresing Xpos value for next agent
            number_waves -= 1  # Decreasing value after each wave sent

        ms2 = int(round(time.time() * 1000))
        xpos = 40  # Since we're using a grid patern, bullets should start at the same point as agents
        # Logic states, if there is no bullet present on screen and if there
        # are still some surviving agents, make new bullets
        if ms2 - ms1 > bullet_time and len(agents) != 0:
            waves_of_bullets += 1
            ms1 = ms2
            just_once = True
            for i in range(
                    CONFIG_DICT['wave_length']):  # Create same number of bullets as number of agents
                # Start them at the same Xpos, but subtract its own size so it
                # centres on the grid and in the straight line with the agent
                bullet = Bullet(x=xpos, y=0, bullet_img=RED_LASER)
                # This line is used to send in a random wave of bullets every
                # time
                if(random.randrange(0, 100)) % 2 == 0:
                    # The bullet is only appended to the bullet_list.
                    # "bullets[]" if the condition is met.
                    bullets.append(bullet)
                    # It is done so that we can have random number of bullets
                    # at random places every wave of bullets
                xpos += xxpos  # Increase Xpos value for next bullet

        for event in pygame.event.get():  # In case someone presses a button
            if event.type == pygame.QUIT:  # If the button pressebd is "X" in the top right to close the window, then the simulation should stop
                pygame.quit()
                sys.exit()
                run = False  # Stop the main while loop on closing

        if len(agents) == 0 and len(bullets) == 0:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and just_once == False:
                agents[0].health = 1
                agents[4].health = 1
                just_once = True

        survived_agents = move_agents(
            agents, survived_agents, CONFIG_DICT['agent_vel'])

        for bullet in bullets:  # Similar loop description as for agents but for bullets
            bullet.move(CONFIG_DICT['bullet_vel'])
            if bullet.y > HEIGHT:  # If bullet goes offscreen when moving downwards, then
                # Remove the bullet from the list of bullets
                bullets.remove(bullet)
                # And since we're in the loop of moving all bullets, we check
                # if they collide with an agent
            for agent in agents:  # Checking for all agents in one go
                try:
                    if collide(
                            agent,
                            bullet):  # If two objects (agent object and bullet object) collide as defined in the function above
                        # print("Hit")
                        # #Print console log "Hit" for testing
                        # Once the bullet hits, we remove it from the
                        # simulation
                        bullets.remove(bullet)
                        # And the agent that the bullet hit gets 1 minus
                        # health.
                        agent.health -= 1
                    if agent.health == 0:  # We check if the agent has 0 hp, that means the agent died.
                        # If agent is dead, we remove it from the screen
                        agents.remove(agent)
                except ValueError:
                    pass
                
        if CONFIG_DICT['communication'] == 'centralized' or CONFIG_DICT['communication'] == 'decentralized':
            if CONFIG_DICT['communication'] == 'centralized':
                agents, bool_loc, bool_config, bool_perm_config, bool_move = centralized_logic(agents, xxpos, CONFIG_DICT, bool_loc, bool_config, bool_perm_config, bool_move)

            for agent in agents[:]:
                for tnega in agents:
                    if agent != tnega:
                        if abs(
                            agent.x -
                            tnega.x) < CONFIG_DICT['cover_radius'] and agent.health == 1 and agent.cover == False and tnega.health != 1 and CONFIG_DICT['to_cover'] == True and tnega.cost != 0:
                            cover(agent, tnega)
                            agent.cover = True
                            tnega.cost -= 1

        # Finally, redraw_window function is called to update every object on
        # the screen for the next frame
        redraw_window()

        end_while_time = datetime.now()
        comp_time = end_while_time - start_while_time
        # Saving in microseconds
        comp_time_to_wave[tick_counter] = comp_time.microseconds

        if len(agents) == 0:
            pygame.quit()
            run = False

    del agents_to_wave[0]
    results_service_obj = ResultService(
        config_dict=CONFIG_DICT,
        num_survived_agents=survived_agents,
        exp_number=exp_number,
        waves_of_bullets=waves_of_bullets,
        agents_to_wave=agents_to_wave,
        comp_time_to_wave=comp_time_to_wave)
    results_service_obj.save_results()
