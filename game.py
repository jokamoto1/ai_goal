from car import Car
from ball import Ball
from goal import Goal
import pygame
import math
import os
import neat
import pickle
import random
from sys import exit

class Game():
    def __init__(self,screen,clock):
        self.top_score = 0
        self.bottom_score = 0
        self.total_ticks = 5000
        self.screen = screen
        self.clock = clock


    def ball_collision(self,car, ball):
    
        if pygame.sprite.spritecollide(car.sprite, ball, False):

            ball.sprite.x_velo += car.sprite.x_velo
            ball.sprite.y_velo += car.sprite.y_velo

        
    def goal_collision(self, ball,goal,top_car,bottom_car):
        if pygame.sprite.spritecollide(goal.sprite, ball, False):
            if goal.sprite.location == 'top':
                self.bottom_score +=1
            else:
                self.top_score +=1
            ball.sprite.reset()
            top_car.sprite.reset()
            bottom_car.sprite.reset()
    def collision_between_two_sprites(self,sprite1,sprite2):
        sprite1 = sprite1.sprite
        sprite2 = sprite2.sprite
        right1 = (sprite1.rect.centerx + sprite1.rect.width/2)
        left1 = (sprite1.rect.centerx - sprite1.rect.width/2)
        top1 = (sprite1.rect.centery + sprite1.rect.height/2)
        bottom1 = (sprite1.rect.centery - sprite1.rect.height/2)

        right2 = (sprite2.rect.centerx + sprite2.rect.width/2)
        left2 = (sprite2.rect.centerx - sprite2.rect.width/2)
        top2 = (sprite2.rect.centery + sprite2.rect.height/2)
        bottom2= (sprite2.rect.centery - sprite2.rect.height/2)

        collision_tolerance =10
        if pygame.sprite.collide_rect(sprite1,sprite2):
    
            if abs(top1- bottom2) < collision_tolerance:
                sprite1.rect.centery -= 7
                sprite2.rect.centery += 7

            if abs(bottom1 - top2) < collision_tolerance:
                sprite2.rect.centery -= 7
                sprite1.rect.centery +=7
      

            if abs(right1 - left2) < collision_tolerance:
                sprite1.rect.centerx -= 7
                sprite2.rect.centerx +=7
        
            if abs(left1 - right2) < collision_tolerance:
                sprite2.rect.centerx -= 7
                sprite1.rect.centerx += 7
    def collision_between_car_and_ball(self,sprite1,sprite2):
        sprite1 = sprite1.sprite
        sprite2 = sprite2.sprite
        right1 = (sprite1.rect.centerx + sprite1.rect.width/2)
        left1 = (sprite1.rect.centerx - sprite1.rect.width/2)
        top1 = (sprite1.rect.centery + sprite1.rect.height/2)
        bottom1 = (sprite1.rect.centery - sprite1.rect.height/2)

        right2 = (sprite2.rect.centerx + sprite2.rect.width/2)
        left2 = (sprite2.rect.centerx - sprite2.rect.width/2)
        top2 = (sprite2.rect.centery + sprite2.rect.height/2)
        bottom2= (sprite2.rect.centery - sprite2.rect.height/2)

        collision_tolerance =15
        if pygame.sprite.collide_rect(sprite1,sprite2):
    
            if abs(top1- bottom2) < collision_tolerance:
         
                sprite2.rect.centery += 8

            if abs(bottom1 - top2) < collision_tolerance:
                sprite2.rect.centery -= 8
        
      

            if abs(right1 - left2) < collision_tolerance:
          
                sprite2.rect.centerx +=8
        
            if abs(left1 - right2) < collision_tolerance:
                sprite2.rect.centerx -= 8
            






    def train_ai(self, genome1,genome2,config):
        topnet = neat.nn.FeedForwardNetwork.create(genome1, config)
        botnet = neat.nn.FeedForwardNetwork.create(genome2, config)


        bottom_car = pygame.sprite.GroupSingle()
        bottom_car.add(Car('red', 500/2, 500, True))

        top_car = pygame.sprite.GroupSingle()
        top_car.add(Car('blue', 500/2, 100,True))
        

        ball = pygame.sprite.GroupSingle()
        ball.add(Ball(500/2, 600/2))


        top_goal = pygame.sprite.GroupSingle()
        top_goal.add(Goal(500/2, 0, 'top'))

        bottom_goal = pygame.sprite.GroupSingle()
        bottom_goal.add(Goal(500/2, 580, 'bottom'))

        while True and self.total_ticks >0:

            topnetx,topnety = topnet.activate((top_car.sprite.rect.centerx,top_car.sprite.rect.centery,bottom_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))
            botnetx,botnety = botnet.activate((bottom_car.sprite.rect.centerx,bottom_car.sprite.rect.centery,top_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))


            # print(self.total_ticks)
            self.screen.fill('white')
            self.total_ticks -=1
    

            self.ball_collision(top_car,ball)
            self.ball_collision(bottom_car,ball)
            self.collision_between_car_and_ball(top_car,ball)

            self.collision_between_car_and_ball(bottom_car,ball)
  
            self.collision_between_two_sprites(bottom_car,top_car)

            
            self.goal_collision(ball,top_goal,top_car,bottom_car)
            self.goal_collision(ball,bottom_goal,top_car,bottom_car)

            ball.update()
            bottom_car.update(botnetx,botnety)
            top_car.update(topnetx,topnety)

            ball.draw(self.screen)
            bottom_car.draw(self.screen)
            top_car.draw(self.screen)
            top_goal.draw(self.screen)
            bottom_goal.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            self.clock.tick(60)
            pygame.display.update()
           