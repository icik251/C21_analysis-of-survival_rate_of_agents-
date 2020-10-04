import pygame
import os
import time
import random
pygame.font.init()       #To show counter, font needs to be initialized

#Set window width/height and name of window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))         			  #The main window to show the running simulation
pygame.display.set_caption("Agent Simulation")

#Load assets
RED_AGENT = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
#Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
#Backgrond
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))


#This full class defines agents, each with its own attributes
class Agent:         
	def __init__(self, x, y, health=3):
		self.x = x                                                #X-coordinate for each of the agent present in the list
		self.y = y 						  #Y-coordinate for each of the agent present in the list
		self.health = health
		self.ship_img = RED_AGENT
		self.mask = pygame.mask.from_surface(self.ship_img)       #Mask is used to check for pixel perfect collisions
		self.max_health = health

	def draw(self, window):                                       	  #To show/draw the agent on the screen
		window.blit(self.ship_img, (self.x, self.y))		  #Draw agent image at its own x/y coordinate
		self.healthbar(window)					  #Also draw the healthbar for each agent


	def move(self, vel):						  #To move the agent on the screen every loop
		self.y -= vel 						  #Since y increases as you move down in pygame screen, so we reduce y to move up

	def get_width(self):
		return self.ship_img.get_width()
	def get_height(self):
		return self.ship_img.get_height()

	def healthbar(self, window):					  #Healthbar for each of the agent
		pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width(), 10))
		pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


#This full class defines the bullets/lasers
class Bullet:
	def __init__(self, x, y, health=3):
		self.x = x
		self.y = y
		self.health = health
		self.bullet_img = RED_LASER
		self.mask = pygame.mask.from_surface(self.bullet_img)

	def draw(self, window):
		window.blit(self.bullet_img, (self.x, self.y))

	def move(self, vel):
		self.y += vel


def collide(obj1, obj2):                                        		#Collide function is used to check for pixel perfect collisions using masks
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))


def main():
	run = True   								#To make the main loop run
	FPS = 60     								#Pygame FPS
	counter = 0 								#Count the number of agents surviving
	main_font = pygame.font.SysFont("comicsans", int(WIDTH/25))		#Usint the font to display surviving agents
	agents = []								#List to store all the agents on screen
	agent_vel = 3								#Agent velocity when moving up
	bullets = []								#List to store all the bullets on the screen
	bullet_vel = 5								#Enemy bullet velocity moving downwards
	clock = pygame.time.Clock()						#An object to help track time, will be used to run pygame on specific FPS

	def redraw_window():   							#This function can only be called in "main" Function. Basically updates window every frame
		WIN.blit(BG,(0,0))  						#blit draws the image on the background at the given coordinates
		
		#Drawing counter on the screen
		counter_label = main_font.render(f"Agents Survived: {counter}", 1, (255,255,255))
		WIN.blit(counter_label, (10, 10))

		for agent in agents:
			agent.draw(WIN)						#Every screen update, draw the agents present in the agents[] list on the screen
		for bullet in bullets:						#Every screen update, draw the bullets present in the bullets[] list on screen
			bullet.draw(WIN)

		pygame.display.update() 					#Updates the entire surface/screen every loop

	no_of_waves = 1								#The number of waves that will try to cross the line
	
	while run:
		clock.tick(FPS)   						#Means that for every second at most "FPS" frames should pass. Here, FPS = 60
		wave_length = 5							#Number of agents present in one wave
		xpos = 200							#X-Position of the initial agent. Hard coded for now

		if len(agents) == 0 and no_of_waves>0:						#Logic states, If there is no agent on the screen and the required number of waves have not gone already, send in the next wave
			for i in range(wave_length):						#initialising to run the loop "length" number of times to create the required number of agents
				agent = Agent(xpos, random.randrange(HEIGHT, HEIGHT+10))	#Start first agent at X=200, and thereafter at 100+ from previous X pos.
				agents.append(agent)						#Add the new initialized agent to the agent list
				xpos += 100							#incresing Xpos value for next agent
			no_of_waves -= 1							#Decreasing value after each wave sent
				
		xpos = 200									#Since we're using a grid patern, bullets should start at the same point as agents
		if len(bullets) == 0 and len(agents)!= 0:					#Logic states, if there is no bullet present on screen and if there are still some surviving agents, make new bullets
			for i in range(wave_length):						#Create same number of bullets as number of agents			
				bullet = Bullet(xpos-15, 0)					#Start them at the same Xpos, but subtract its own size so it centres on the grid and in the straight line with the agent
				if(random.randrange(0,100))%2==0:				#This line is used to send in a random wave of bullets every time
					bullets.append(bullet)					#The bullet is only appended to the bullet_list "bullets[]" if the condition is met.
												#It is done so that we can have random number of bullets at random places every wave of bullets
				xpos += 100							#Increase Xpos value for next bullet

		for event in pygame.event.get():						#Incase someone presses a button
			if event.type == pygame.QUIT:						#If the button pressed is "X" in the top right to close the window, then the simulation should stop
				run = False   							#Stop the main while loop on closing

		for agent in agents[:]:								#Loop to update position of every agent every frame (To make them move up)
			agent.move(agent_vel)							#Move agent up with the velocity defined
			if agent.y < 0:								#A statement to see if the Agent crosses the line(which is y = 0), then
				counter += 1							#increase the count of agents survived
				agents.remove(agent)						#And remove the agent from the list of agents as it is now offscreen

		for bullet in bullets[:]:							#Similar loop description as for agents but for bullets
			bullet.move(bullet_vel)
			if bullet.y > HEIGHT:							#If bullet goes offscreen when moving downwards, then
				bullets.remove(bullet)						#Remove the bullet from the list of bullets
													#And since we're in the loop of moving all bullets, we check if they collide with an agent
			for agent in agents:									#Checking for all agents in one go
				if collide(agent,bullet):							#If two objects (agent object and bullet object) collide as defined in the function above
					#print("Hit")								#Print console log "Hit" for testing					
					bullets.remove(bullet)							#Once the bullet hits, we remove it from the simulation
					agent.health -= 1							#And the agent that the bullet hit gets 1 minus health.
				if agent.health == 0:								#We check if the agent has 0 hp, that means the agent died.
					agents.remove(agent)							#If agent is dead, we remove it from the screen

		redraw_window()									#Finally, redraw_window function is called to update every object on the screen for the next frame
	
main() #Calling main function to start running the simulation.
