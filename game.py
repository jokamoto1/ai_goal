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
        self.top_score_real = 0
        self.bottom_score_real = 0
        self.total_ticks = 1200
        self.screen = screen
        self.clock = clock


    def ball_collision(self,car, ball):
    
        if pygame.sprite.spritecollide(car.sprite, ball, False):

            ball.sprite.x_velo += car.sprite.x_velo *2
            ball.sprite.y_velo += car.sprite.y_velo *2
            return True
        else:
            return False

        
    def goal_collision(self, ball,goal,top_car,bottom_car):
        if pygame.sprite.spritecollide(goal.sprite, ball, False):
            if goal.sprite.location == 'top':
                self.bottom_score +=10
                self.bottom_score_real +=1
            else:
                self.top_score +=10
                self.top_score_real +=1
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

        topcarxy = (0,0)
        botcarxy = (0,0)

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
            botnetx,botnety = topnet.activate((bottom_car.sprite.rect.centerx,bottom_car.sprite.rect.centery,top_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))
            
            
            self.total_ticks -=1
    

            if  self.ball_collision(top_car,ball):
                self.top_score += .0005
            if  self.ball_collision(bottom_car,ball):
                self.bottom_score +=.0005

            self.collision_between_car_and_ball(top_car,ball)

            self.collision_between_car_and_ball(bottom_car,ball)
  
            self.collision_between_two_sprites(bottom_car,top_car)

            
            self.goal_collision(ball,top_goal,top_car,bottom_car)
            self.goal_collision(ball,bottom_goal,top_car,bottom_car)


            

            ball.update()
            bottom_car.update(botnetx,botnety)
            top_car.update(topnetx,topnety)


            if top_car.sprite.rect.center == topcarxy:
                self.top_score -=.002
            if bottom_car.sprite.rect.center == botcarxy:
                self.bottom_score -=.002
            topcarxy = top_car.sprite.rect.center
            botcarxy = bottom_car.sprite.rect.center

            # self.screen.fill('white')
            # ball.draw(self.screen)
            # bottom_car.draw(self.screen)
            # top_car.draw(self.screen)
            # top_goal.draw(self.screen)
            # bottom_goal.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            # self.clock.tick(60)
            # pygame.display.update()

    def fight_ai(self, genome1,config):
        topnet = neat.nn.FeedForwardNetwork.create(genome1, config)


        bottom_car = pygame.sprite.GroupSingle()
        bottom_car.add(Car('red', 500/2, 500, False))

        top_car = pygame.sprite.GroupSingle()
        top_car.add(Car('blue', 500/2, 100,True))
        

        ball = pygame.sprite.GroupSingle()
        ball.add(Ball(500/2, 600/2))


        top_goal = pygame.sprite.GroupSingle()
        top_goal.add(Goal(500/2, 0, 'top'))

        bottom_goal = pygame.sprite.GroupSingle()
        bottom_goal.add(Goal(500/2, 580, 'bottom'))

        font = pygame.font.Font(None, 25)
        
        while True and self.total_ticks >0:

            topnetx,topnety = topnet.activate((top_car.sprite.rect.centerx,top_car.sprite.rect.centery,bottom_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))
            

    

            self.ball_collision(top_car,ball)
                
            self.ball_collision(bottom_car,ball)
               
            self.collision_between_car_and_ball(top_car,ball)

            self.collision_between_car_and_ball(bottom_car,ball)
  
            self.collision_between_two_sprites(bottom_car,top_car)

            
            self.goal_collision(ball,top_goal,top_car,bottom_car)
            self.goal_collision(ball,bottom_goal,top_car,bottom_car)


            

            ball.update()
            bottom_car.update(1,1)
            top_car.update(topnetx,topnety)



            self.screen.fill('white')
            top_score_surf = font.render(f'Blue Score: {self.top_score_real}', False, 'Blue')
            bottom_score_surf = font.render(f'Red Score: {self.bottom_score_real}', False, 'Red')
            top_score_rect = top_score_surf.get_rect(topleft = (0,0))
            bottom_score_rect = bottom_score_surf.get_rect(bottomleft = (0,600))
            self.screen.blit(top_score_surf, top_score_rect)
            self.screen.blit(bottom_score_surf, bottom_score_rect)

            ball.draw(self.screen)
            bottom_car.draw(self.screen)
            top_car.draw(self.screen)
            top_goal.draw(self.screen)
            bottom_goal.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:
                        ball.sprite.reset()
                        top_car.sprite.reset()
                        bottom_car.sprite.reset()
            self.clock.tick(60)
            pygame.display.update()
    def ai_vs_ai(self, genome1,genome2,config):
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

            font = pygame.font.Font(None, 25)
            
            while True and self.total_ticks >0:

                topnetx,topnety = topnet.activate((top_car.sprite.rect.centerx,top_car.sprite.rect.centery,bottom_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))
                botnetx,botnety = botnet.activate((bottom_car.sprite.rect.centerx,bottom_car.sprite.rect.centery,top_goal.sprite.rect.centery,ball.sprite.rect.centerx,ball.sprite.rect.centerx))


        

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



                self.screen.fill('white')
                top_score_surf = font.render(f'Blue Score: {self.top_score_real}', False, 'Blue')
                bottom_score_surf = font.render(f'Red Score: {self.bottom_score_real}', False, 'Red')
                top_score_rect = top_score_surf.get_rect(topleft = (0,0))
                bottom_score_rect = bottom_score_surf.get_rect(bottomleft = (0,600))
                self.screen.blit(top_score_surf, top_score_rect)
                self.screen.blit(bottom_score_surf, bottom_score_rect)

                ball.draw(self.screen)
                bottom_car.draw(self.screen)
                top_car.draw(self.screen)
                top_goal.draw(self.screen)
                bottom_goal.draw(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            ball.sprite.reset()
                            top_car.sprite.reset()
                            bottom_car.sprite.reset()
                self.clock.tick(60)
                pygame.display.update()
                    