import pygame

class Agent:
    def __init__(self, x, y, config_dict, ship_img):

        """ This full class defines the bullets/lasers

            x:
                The coordinate for x axis.
            y:
                The coordinate for y axis.
            bullet_img:
                The loaded bullet image.
        """

        self.x = x  
        self.y = y
        self.ship_img = ship_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.health = 3
        self.max_health = 3
        self.cover = False
        self.cost = config_dict['cost_value']
        self.max_cost = config_dict['cost_value']
        self.show_covering = config_dict['show_covering']
        self.cover_radius = config_dict['cover_radius']

    def draw(self, window):
        """ Show/draw the agent on the screen.

            window:
                The window object.
        """
        # Draw agent image at its own x/y coordinate.
        window.blit(self.ship_img, (self.x, self.y))
        # Also draw the healthbar for each agent.
        self.healthbar(window)
        # if you dont want to see battery health bar comment this line.
        self.battery_healthbar(window)

    def move(self, vel):
        """ To move the agent on the screen every loop

            vel:
                The velocity by which it will move
        """
        # Since y increases as you move down in pygame screen, so we reduce y to move up
        self.y -= vel

    def get_width(self):
        """
            Get width.
        """
        return self.ship_img.get_width()

    def get_height(self):
        """
            Get height.
        """
        return self.ship_img.get_height()

    def battery_healthbar(self, window):
        """
            Draw the bbatery and healthbar.

            window:
                The window object.
        """
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

    def healthbar(self, window):
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
        """
            Check if show covering parameter is set to True.
        """                                       
        if self.show_covering:
            pygame.draw.circle(window,
                               (0,
                                0,
                                255),
                               (int(self.x + self.get_width() / 2),
                                int(self.y + self.get_height() / 2)),
                               self.cover_radius,
                               1)