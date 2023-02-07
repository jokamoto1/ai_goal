import pygame
import math

class Car(pygame.sprite.Sprite):
    def __init__(self,color,x_inital,y_initial,ai):
        super().__init__()
        self.image = pygame.image.load(f'images/{color}car.png').convert_alpha()
        self.image2 = pygame.image.load(f'images/{color}car.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x_inital,y_initial))
        self.orginalx = x_inital
        self.orignaly = y_initial
        self.score = 0
        self.x_velo = 0
        self.y_velo = 0
        self.ai = ai
    def rot_center(self, image, rect, angle):

        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
    
    def movement_player(self):
        keys = pygame.key.get_pressed()
        if self.x_velo < 5/2:
            if keys[pygame.K_d]:
                self.x_velo +=1/2
        if self.x_velo > -5/2:
            if keys[pygame.K_a]:
                self.x_velo -=1/2
        if self.y_velo > -5:
            if keys[pygame.K_w]:
                self.y_velo -=1/2
        if self.y_velo < 5:
            if keys[pygame.K_s]:
                self.y_velo +=1/2
    def movement_ai(self, x,y):
        if self.x_velo < 5:
            if x > .6:
                self.x_velo +=1
        if self.x_velo > -5:
            if x < .3:
                self.x_velo -=1
        if self.y_velo > -5:
            if y <.3:
                self.y_velo -=1
        if self.y_velo < 5:
            if  y >.6:
                self.y_velo +=1   

    
    def drag(self):
        if self.x_velo > 0:
            self.x_velo -=.1
        if self.x_velo < 0:
            self.x_velo +=.1
        if self.y_velo > 0:
            self.y_velo -=.1
        if self.y_velo < 0:
            self.y_velo +=.1
    def in_bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 500:
            self.rect.right = 500
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
    def animate_direction(self):
        dx, dy = self.x_velo,  self.y_velo
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image, self.rect = self.rot_center(self.image2, self.rect, angle)

    def reset(self):
        self.rect.center = self.orginalx,self.orignaly
        self.x_velo = 0
        self.y_velo =0

    def update(self,x,y):
        if not self.ai:
            self.movement_player()
        else:
            self.movement_ai(x,y)
        self.drag()
        self.animate_direction()
        self.rect.centerx += self.x_velo
        self.rect.centery += self.y_velo
        self.in_bounds()
    

