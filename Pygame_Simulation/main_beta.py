import pygame
import os
import time
import random
from json_service import JsonService
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Read json dict
json_service_obj = JsonService()
config_dict = json_service_obj.get_json_dict()

random.seed(3)
pygame.font.init()  # To show counter, font needs to be initialized

# Set window width/height and name of window
WIDTH, HEIGHT = 1000, 800
# The main window to show the running simulation
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agent Simulation")

run = True  # To make the main loop run
FPS = 120  # Pygame FPS
counter = 0  # Count the number of agents surviving
# Using the font to display surviving agents
main_font = pygame.font.SysFont("comicsans", int(WIDTH / 25))
agents = []  # List to store all the agents on screen
bullets = []  # List to store all the bullets on the screen
# An object to help track time, will be used to run pygame on specific FPS
clock = pygame.time.Clock()
bullet_time = 1250 / config_dict['sim_speed']  # milisecond
xpos = 40
xxpos = int((WIDTH - xpos * 2) / (config_dict['wave_length'] - 1))
number_waves = config_dict['no_of_waves']

# Load assets
RED_AGENT = pygame.transform.scale(pygame.image.load(os.path.join(
    "Pygame_Simulation\\assets", "pixel_ship_red_small.png")), (40, 30))
#RED_AGENT = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
# Lasers
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join(
    "Pygame_Simulation\\assets", "pixel_laser_red.png")), (50, 40))
#RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
# Backgrond
BG = pygame.transform.scale(
    pygame.image.load(
        os.path.join(
            "Pygame_Simulation\\assets",
            "background-black.png")),
    (WIDTH,
     HEIGHT))


# This full class defines agents, each with its own attributes
class Agent:
    def __init__(self, x, y, health=3, cover=False,
                 cost=config_dict['cost_value']):
        self.x = x  # X-coordinate for each of the agent present in the list
        self.y = y  # Y-coordinate for each of the agent present in the list
        self.health = health
        self.ship_img = RED_AGENT
        # Mask is used to check for pixel perfect collisions
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.cover = False
        self.cost = cost
        self.max_cost = cost

    def draw(self, window):  # To show/draw the agent on the screen
        # Draw agent image at its own x/y coordinate
        window.blit(self.ship_img, (self.x, self.y))
        self.healthbar(window)  # Also draw the healthbar for each agent
        # if you dont want to see battery health bar comment this line
        self.battery_healthbar(window)

    def move(self, vel):  # To move the agent on the screen every loop
        self.y -= vel  # Since y increases as you move down in pygame screen, so we reduce y to move up

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def battery_healthbar(self, window):
        pygame.draw.rect(
            window,
            (255,
             0,
             0),
            (self.x,
             self.y +
             self.get_height() +
             20,
             self.ship_img.get_width(),
             10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y +
                                               self.get_height() +
                                               20, self.ship_img.get_width() *
                                               (self.cost /
                                                   self.max_cost), 10))

    def healthbar(self, window):  # Healthbar for each of the agent
        pygame.draw.rect(
            window,
            (255,
             0,
             0),
            (self.x,
             self.y +
             self.get_height() +
             5,
             self.ship_img.get_width(),
             5))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y +
                                               self.get_height() +
                                               5, self.ship_img.get_width() *
                                               (self.health /
                                                self.max_health), 5))
        #pygame.draw.circle(window, (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)), (self.x + int(self.get_width()/2), self.y + int(self.get_height()/2)), 150, 1)
        if config_dict['show_covering']:
            pygame.draw.circle(window,
                               (0,
                                0,
                                255),
                               (int(self.x + self.get_width() / 2),
                                int(self.y + self.get_height() / 2)),
                               config_dict['cover_radius'],
                               1)


# This full class defines the bullets/lasers
class Bullet:
    def __init__(self, x, y, health=3):
        self.x = x
        self.y = y
        self.health = health
        self.bullet_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.bullet_img)

    def draw(self, window):
        window.blit(self.bullet_img, (self.x - 5, self.y))

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):  # Collide function is used to check for pixel perfect collisions using masks
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))


def move_agents(agents, counter, agent_vel):
    # Loop to update position of every agent every frame (To make them move up)
    for agent in agents[:]:
        agent.move(agent_vel)  # Move agent up with the velocity defined
        # A statement to see if the Agent crosses the line(which is y = 0),
        # then
        if agent.y < 150:
            counter += 1  # increase the count of agents survived
            # And remove the agent from the list of agents as it is now
            # offscreen
            agents.remove(agent)
    return counter


def cover(obj1, obj2):
    # print(obj1.cover)
    if not obj1.cover:
        obj2.x = obj1.x
        obj2.y = obj1.y
        obj2.y -= 80


def save_results(
        main_parameter='',
        parameter_value=None,
        exp_number=None,
        waves_of_bullets=None):
    if not os.path.exists('Experiments'):
        os.makedirs('Experiments')

    # Check if arguments are passed
    if main_parameter == '' or parameter_value is None or exp_number is None:
        print(main_parameter)
        print(parameter_value)
        print(exp_number)
        return 1

    dir_name = 'Experiments\\{}_{}\\'.format(main_parameter, parameter_value)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    text_file = open(dir_name + 'exp_{}.txt'.format(exp_number), "w")
    text_file.write(
        "Number of Initial Agents: %s \nNumber of Agents survived: %s \nNumber of wave of bullets fired: %s \n" %
        (config_dict['wave_length'], counter, waves_of_bullets))
    text_file.write("\n")
    text_file.write("Variables Used \n")
    text_file.write(
        "Agent Velocity: %s\n" %
        (config_dict['agent_vel'] *
         config_dict['sim_speed']))
    text_file.write(
        "Bullet Velocity: %s\n" %
        (config_dict['bullet_vel'] *
         config_dict['sim_speed']))
    text_file.write("Number of Agents: %s\n" % config_dict['wave_length'])
    text_file.write("Number of Waves: %s\n" % number_waves)
    text_file.write("Covering Radius: %s\n" % config_dict['cover_radius'])
    text_file.write("Agent covering (Boolean): %s\n" % config_dict['to_cover'])
    text_file.write("Cost Function Value: %s\n" % config_dict['cost_value'])
    text_file.close()


def main(main_parameter='', parameter_value=None, exp_number=None):

    def redraw_window():  # This function can only be called in "main" Function. Basically updates window every frame
        # blit draws the image on the background at the given coordinates
        WIN.blit(BG, (0, 0))

        # Drawing counter on the screen
        counter_label = main_font.render(
            f"Agents Survived: {counter}", 1, (255, 255, 255))
        WIN.blit(counter_label, (10, 10))
        pygame.draw.line(WIN, (255, 0, 0), (0, 150), (WIDTH, 150), 2)

        for agent in agents:
            # Every screen update, draw the agents present in the agents[] list
            # on the screen
            agent.draw(WIN)
        for bullet in bullets:  # Every screen update, draw the bullets present in the bullets[] list on screen
            bullet.draw(WIN)

        pygame.display.update()  # Updates the entire surface/screen every loop

    global run
    global counter
    global number_waves
    waves_of_bullets = 0
    ms1 = int(round(time.time() * 1000))

    just_once = False
    while run:
        # Means that for every second at most "FPS" frames should pass. Here,
        # FPS = 60
        clock.tick(FPS)

        xpos = 40  # X-Position of the initial agent. Hard coded for now

        # Logic states, If there is no agent on the screen and the required
        # number of waves have not gone already, send in the next wave
        if len(agents) == 0 and number_waves > 0:
            # initialising to run the loop "length" number of times to create
            # the required number of agents
            for i in range(config_dict['wave_length']):
                agent = Agent(xpos, random.randrange(HEIGHT - 100, HEIGHT))
                # Add the new initialized agent to the agent list
                agents.append(agent)
                xpos += xxpos  # incresing Xpos value for next agent
            number_waves -= 1  # Decreasing value after each wave sent

        ms2 = int(round(time.time() * 1000))
        xpos = 40  # Since we're using a grid patern, bullets should start at the same point as agents
        # if len(bullets) == 0 and len(agents)!= 0:
        # #Logic states, if there is no bullet present on screen and if there
        # are still some surviving agents, make new bullets
        if ms2 - ms1 > bullet_time and len(agents) != 0:
            waves_of_bullets += 1
            ms1 = ms2
            just_once = True
            for i in range(
                    config_dict['wave_length']):  # Create same number of bullets as number of agents
                # Start them at the same Xpos, but subtract its own size so it
                # centres on the grid and in the straight line with the agent
                bullet = Bullet(xpos, 0)
                # This line is used to send in a random wave of bullets every
                # time
                if(random.randrange(0, 100)) % 2 == 0:
                    # The bullet is only appended to the bullet_list
                    # "bullets[]" if the condition is met.
                    bullets.append(bullet)
                    # It is done so that we can have random number of bullets
                    # at random places every wave of bullets
                xpos += xxpos  # Increase Xpos value for next bullet

        for event in pygame.event.get():  # Incase someone presses a button
            if event.type == pygame.QUIT:  # If the button pressebd is "X" in the top right to close the window, then the simulation should stop
                pygame.quit()
                sys.exit()
                run = False  # Stop the main while loop on closing

        if len(agents) == 0 and len(bullets) == 0:
            run = False

        # if not just_once:
            #agents[3].health = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and just_once == False:
                agents[0].health = 1
                agents[4].health = 1
                just_once = True

        counter = move_agents(agents, counter, config_dict['agent_vel'])

        for bullet in bullets:  # Similar loop description as for agents but for bullets
            bullet.move(config_dict['bullet_vel'])
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

        for agent in agents[:]:
            for tnega in agents:
                if agent != tnega:
                    if abs(
                            agent.x -
                            tnega.x) < config_dict['cover_radius'] and agent.health == 1 and agent.cover == False and tnega.health != 1 and config_dict['to_cover'] == True and tnega.cost != 0:
                        cover(agent, tnega)
                        #print("agent index = "+str(agents.index(agent)))
                        agent.cover = True
                        tnega.cost -= 1

        # time.sleep(0.5)
        redraw_window()  # Finally, redraw_window function is called to update every object on the screen for the next frame
        if len(agents) == 0:
            pygame.quit()
            run = False
    # pygame.quit()
    save_results(
        main_parameter=main_parameter,
        parameter_value=parameter_value,
        exp_number=exp_number,
        waves_of_bullets=waves_of_bullets)

# For running one experiment
# main()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run drone simulatiom')
    parser.add_argument('--main_parameter', required=False,
                        help='parameter name that does not change')
    parser.add_argument('--parameter_value', required=False,
                        help='value of the parameter')
    parser.add_argument('--exp_number', required=False,
                        help='number of experiment')
    args = parser.parse_args()
    main(
        main_parameter=args.main_parameter,
        parameter_value=args.parameter_value,
        exp_number=args.exp_number)
