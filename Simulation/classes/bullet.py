import pygame

class Bullet:
    def __init__(self, x, y, bullet_img):
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
        self.health = 3
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.bullet_img)

    def draw(self, window):
        """ Show/draw the bullet on the screen.

            window:
                The window object.
        """
        window.blit(self.bullet_img, (self.x - 5, self.y))

    def move(self, vel):
        """ To move the bullet on the screen every loop

            vel:
                The velocity by which it will move
        """
        self.y += vel