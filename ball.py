import pygame
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self,x_initial,y_initial):
        super().__init__()
        self.image = pygame.image.load(f'images/ball.png').convert_alpha()
        self.image2 = pygame.image.load(f'images/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x_initial,y_initial))
        self.original_x = x_initial
        self.original_y = y_initial
        self.x_velo = 0
        self.y_velo =  0

    def rot_center(self, image, rect, angle):

        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
    def drag(self):
        if self.x_velo > 0:
            self.x_velo -=.1/2
        if self.x_velo < 0:
            self.x_velo +=.1/2
        if self.y_velo > 0:
            self.y_velo -=.1/2
        if self.y_velo < 0:
            self.y_velo +=.1/2
    def in_bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 1
            self.x_velo *= -1
        if self.rect.right >= 500:
            self.rect.right = 499
            self.x_velo *= -1
        if self.rect.top <= 0:
            self.rect.top = 1
            self.y_velo *= -1
        if self.rect.bottom >= 600:
            self.rect.bottom = 599
            self.y_velo *= -1

    def move(self):
        if self.x_velo > 10/2:
            self.x_velo =10/2
        if self.y_velo > 10/2:
            self.y_velo =10/2
        if self.x_velo < -10/2:
            self.x_velo =-10/2
        if self.y_velo < -10/2:
            self.y_velo =-10/2

        self.rect.centerx += self.x_velo
        self.rect.centery += self.y_velo


    def animate_direction(self):
        dx, dy = self.x_velo,  self.y_velo
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image, self.rect = self.rot_center(self.image2, self.rect, angle)        
    def reset(self):

        self.rect.center = self.original_x,self.original_y
        self.y_velo = 0
        self.x_velo = 0

    def update(self):
        self.drag()
        self.move()
        # self.animate_direction()
        self.in_bounds()