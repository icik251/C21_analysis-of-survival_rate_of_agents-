import pygame
import os
import time
import random
pygame.font.init()

#Set window width/height and name of window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agent Simulation")

#Load assets
RED_AGENT = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
#Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
#Backgrond
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))



class Agent:
	def __init__(self, x, y, health=3):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = RED_AGENT
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

	def draw(self, window):
		#pygame.draw.rect(window, (255,0,0), (self.x, self.y, 20, 20))
		window.blit(self.ship_img, (self.x, self.y))
		self.healthbar(window)


	def move(self, vel):
		self.y -= vel

	def get_width(self):
		return self.ship_img.get_width()
	def get_height(self):
		return self.ship_img.get_height()

	def healthbar(self, window):
		pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width(), 10))
		pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


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


def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))



def main():
	run = True   #To make the main loop run
	FPS = 60     #Pygame FPS
	counter = 0
	main_font = pygame.font.SysFont("comicsans", int(WIDTH/25))

	agents = []
	agent_vel = 1
	bullets = []
	bullet_vel = 5



	#agent = Agent(300, 250)   #Location agent spawns at


	clock = pygame.time.Clock()

	def redraw_window():   #This function can only be called in this function
		WIN.blit(BG,(0,0))  #blit draws the image on the background at the given coordinates
		
		#Draw text
		counter_label = main_font.render(f"Agents Survived: {counter}", 1, (255,255,255))
		WIN.blit(counter_label, (10, 10))

		

		for agent in agents:
			agent.draw(WIN)

		for bullet in bullets:
			bullet.draw(WIN)

		pygame.display.update() #This refreshes the display


	ms1 = int(round(time.time() * 1000))
	no_of_waves = 1
	removed = False
	while run:
		clock.tick(FPS)   #The clock moves with the FPS

		
		
		#print((ms2-ms1)%2000)

		wave_length = 5

		
		
		xpos = 200
		if len(agents) == 0 and no_of_waves>0:	
			for i in range(wave_length):
				
				#agent = Agent(random.randrange(50, WIDTH -100), random.randrange(WIDTH+1,WIDTH+2))
				agent = Agent(xpos, random.randrange(HEIGHT, HEIGHT+10))
				agents.append(agent)
				xpos += 100
			no_of_waves -= 1
				
		xpos = 200		
		#if len(bullets) == 0 and len(agents)!= 0:	
		ms2 = int(round(time.time() * 1000))
		
		#if ((ms2 - ms1)%2000 < 25) and len(agents)!= 0:
		if len(bullets) == 0 and len(agents)!= 0:
			for i in range(wave_length):
				bullet = Bullet(xpos-15, 0)
				if(random.randrange(0,100))%2==0:
					bullets.append(bullet)
				xpos += 100

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False   #Check if someone quits the game

		# k = []
		# ii = random.randrange(1,wave_length)
			
				
		
		# if(removed != True):
		# 	for bullet in bullets[:]:
		# 		if(random.randrange(0,100))%2==0:
		# 			bullets.remove(bullet)
		# 			removed = True

		for agent in agents[:]:
			agent.move(agent_vel)
			if agent.y < 0:
				counter += 1
				agents.remove(agent)



			
			
		

		for bullet in bullets[:]:
			bullet.move(bullet_vel)
			if bullet.y > HEIGHT:
				bullets.remove(bullet)

			for agent in agents:
				#print(agent.get_width())
				if collide(agent,bullet):
					print("hit")
					bullets.remove(bullet)
					agent.health -= 1
				if agent.health == 0:
					agents.remove(agent)

		redraw_window()
	
main()
