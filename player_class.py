import pygame
from settings import *

vec = pygame.math.Vector2

class Player:
    def __init__(self, game, pos):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = vec(self.grid_pos.x*self.game.cell_width + TOPBOTTOMBUFFER // 2 + self.game.cell_width // 2,
                             self.grid_pos.y*self.game.cell_height + TOPBOTTOMBUFFER // 2 + self.game.cell_height // 2)
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.high_score = 0
        self.speed = 2
        self.lives = 0
        self.radius = self.game.cell_width // 2 - 2


    def move(self, direction):
        self.stored_direction = direction

    def draw(self):
        pygame.draw.circle(self.game.screen, GREEN, (int(self.pixel_pos.x), int(self.pixel_pos.y)), self.radius)
        #pygame.draw.rect(self.game.screen, RED, (self.grid_pos.x*self.game.cell_width + TOPBOTTOMBUFFER // 2, 
         #                                        self.grid_pos.y*self.game.cell_height + TOPBOTTOMBUFFER // 2,
          #                                       self.game.cell_width, self.game.cell_height), 1)

        for i in range(self.lives):
            pygame.draw.circle(self.game.screen, GREEN, (40 + 20*i, SCREENHEIGHT - 20), self.radius)


    def update(self):
        if self.able_to_move:
            self.pixel_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        
        self.grid_pos.x = (self.pixel_pos.x - TOPBOTTOMBUFFER +
                            self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos.y = (self.pixel_pos.y - TOPBOTTOMBUFFER +
                            self.game.cell_height // 2) // self.game.cell_height + 1

        if self.grid_pos in self.game.coins:
            self.eat_coin()

    def time_to_move(self):
        if int(self.pixel_pos.x + TOPBOTTOMBUFFER // 2) % self.game.cell_width == 0:
            if self.direction == vec(-1, 0) or self.direction == vec(1, 0):
                return True
        
        if int(self.pixel_pos.y + TOPBOTTOMBUFFER // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, -1) or self.direction == vec(0, 1):
                return True

    def can_move(self):
        if vec(self.grid_pos + self.direction) in self.game.walls:
            return False
        return True
    
    def eat_coin(self):
        self.game.coins.remove(self.grid_pos)
        self.current_score += 1
        if self.current_score >= self.high_score:
            self.high_score = self.current_score

        