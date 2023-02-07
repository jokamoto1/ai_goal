import pygame
class Goal(pygame.sprite.Sprite):
    def __init__(self, x_inital,y_initial,location):
        super().__init__()
        self.image = pygame.image.load('images/goal.png').convert_alpha()
        self.rect = self.image.get_rect(centerx=(x_inital), top = y_initial)
        self.location = location
