import pygame
import random
import numpy as np
from settings import *

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, game, pos, color):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = vec(self.grid_pos.x*self.game.cell_width + self.game.cell_width // 2 + TOPBOTTOMBUFFER // 2,
                             self.grid_pos.y*self.game.cell_height + self.game.cell_height // 2 + TOPBOTTOMBUFFER // 2)
        self.radius = 10
        self.color = color
        self.direction = vec(0, 0)
        self.speed = self.set_speed()

    def draw(self):
        for enemy in self.game.enemies:
            pygame.draw.circle(self.game.screen, self.color, (int(self.pixel_pos.x), int(self.pixel_pos.y)), self.radius)

    def update(self):
        self.pixel_pos += self.direction*self.speed
        if self.time_to_move():
            self.move()
            

        self.grid_pos.x = (self.pixel_pos.x - TOPBOTTOMBUFFER +
                            self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos.y = (self.pixel_pos.y - TOPBOTTOMBUFFER +
                            self.game.cell_height // 2) // self.game.cell_height + 1
            
        
    def move(self):
        if self.color == ORANGE:
           self.direction = self.random_choice()
        elif self.color == RED:
            self.direction = self.get_direction()
        elif self.color == LAVENDER:
           self.direction = self.get_direction()
        elif self.color == AQUA:
           self.direction = self.get_direction()

    def time_to_move(self):
        if int(self.pixel_pos.x + TOPBOTTOMBUFFER // 2) % self.game.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixel_pos.y + TOPBOTTOMBUFFER // 2) % self.game.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False
                        
    def get_direction(self):
        path = self.BFS(self.grid_pos, self.game.player.grid_pos)
        xdir = 0
        ydir = 0
        if self.grid_pos != self.game.player.grid_pos:
            xdir = path[1].x - self.grid_pos.x
            ydir = path[1].y - self.grid_pos.y
        return vec(xdir, ydir)

    def random_choice(self):
        while True:      
            number = random.randint(-2, 2)
            if number == -2:
                direction = vec(-1, 0)
            elif number == -1:
                direction = vec(1, 0)
            elif number == 0:
                direction = vec(0, 1)
            else:
                direction = vec(0, -1)

            if vec(self.grid_pos.x + direction.x, self.grid_pos.y + direction.y) not in self.game.walls:
                break
        return direction
        

    def BFS(self, pos, target):
        queue = []
        queue.append(pos)
        visited = []
        path = []
        current = pos
        while queue:
            if current == target:
                break
            neighbours = [vec(0, 1), vec(0, -1), vec(1, 0), vec(-1, 0)]
            for neighbour in neighbours:
                if (current + neighbour) not in self.game.walls and (current + neighbour) not in visited:
                    queue.append(current + neighbour)
                    path.append({"Current" : current, "Next" : current + neighbour})
            visited.append(current)
            queue.remove(current)
            current = queue[0]
        if queue == None and current != target:
            #print("No solution")
            return None
        else:
            #print("Found target")
            shortest = [target]
            while target != pos:
                for step in path:
                    if step["Next"] == target:
                        target = step["Current"]
                        shortest.insert(0, target)
        return shortest

    def set_speed(self):
        if self.color == RED or self.color == ORANGE:
            return 2
        elif self.color == LAVENDER:
            return 1
        else:
            return 0.75
