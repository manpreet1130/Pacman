import pygame
import sys
from player_class import *
from enemy_class import *
from settings import *

vec = pygame.math.Vector2

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.state = 'intro'
        self.walls = []
        self.coins = []
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.cell_width = WIDTH // 28
        self.cell_height = HEIGHT // 30
        self.enemies = []
        self.load()
        self.player = Player(self, self.player_pos)
        self.high_score = self.player.high_score
        pygame.display.set_caption("Pacman")


    def run(self):
        while self.running:
            if self.state == 'intro':
                self.intro_events()
                self.intro_draw()
                self.intro_update()
            if self.state == 'playing':
                self.playing_events()
                self.playing_draw()
                self.playing_update()
            if self.state == 'over':
                self.over_events()
                self.over_draw()
                self.over_update()
            if self.state == 'winner':
                self.win_events()
                self.win_draw()
                self.win_update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


#--------------HELPER FUNCTIONS------------#

    def draw_text(self, screen, words, font, size, color, pos):
        font = pygame.font.SysFont(font, size)
        text = font.render(words, False, color)
        screen.blit(text, pos)

    def load(self):
        self.maze = pygame.image.load('maze.png')
        self.maze = pygame.transform.scale(self.maze, (WIDTH, HEIGHT))

        with open('layout.txt', 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(x, y))
                    elif char == 'C':
                        self.coins.append(vec(x, y))
                    elif char == 'P':
                        self.player_pos = vec(x, y)
                    elif char == 'a':
                        self.enemies.append(Enemy(self, vec(x, y), RED))
                    elif char == 'b':
                        self.enemies.append(Enemy(self, vec(x, y), ORANGE))
                    elif char == 'c':
                        self.enemies.append(Enemy(self, vec(x, y), AQUA))
                    elif char == 'd':
                        self.enemies.append(Enemy(self, vec(x, y), LAVENDER)) 
                    elif char == "E":
                        pygame.draw.rect(self.maze, BLACK, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))


    def draw_grid(self):
        for i in range(WIDTH // self.cell_width):
            pygame.draw.line(self.maze, GREY, (i*self.cell_width, 0), (i*self.cell_width, HEIGHT))

        for i in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.maze, GREY, (0, i*self.cell_height), (WIDTH, i*self.cell_height))

    #def draw_walls(self):
     #   for wall in self.walls:
      #      pygame.draw.rect(self.maze, BLUE, (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))
        
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE, (int(coin.x*self.cell_width) + TOPBOTTOMBUFFER // 2 + self.cell_width // 2,
                                                    int(coin.y*self.cell_height) + TOPBOTTOMBUFFER // 2 + self.cell_height // 2), 2)
                                            
    
    def game_reset(self):
        self.enemies = []
        self.coins = []
        self.load()
        self.player = Player(self, self.player_pos)


#--------------INTRO FUNCTIONS--------------#

    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'playing'

    def intro_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "PRESS ENTER TO PLAY", INTROTEXTFONT, INTROTEXTSIZE, INTROTEXTCOLOR, INTROTEXTPOS)
        self.draw_text(self.screen, "PRESS ESCAPE TO PLAY", INTROTEXTFONT, INTROTEXTSIZE, INTROTEXTCOLOR, ENTERTEXTPOS)
        self.draw_text(self.screen, "HIGH SCORE : {}".format(self.high_score), HSCOREFONT, HSCORESIZE, WHITE, HSCOREPOS)
        self.intro_update()

    def intro_update(self):
        pygame.display.update()


#--------------PLAYING FUNCTIONS--------------#

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                elif event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                elif event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))


    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.maze, (TOPBOTTOMBUFFER // 2, TOPBOTTOMBUFFER // 2))
        #self.draw_grid()
        #self.draw_walls()
        self.draw_coins()
        self.draw_text(self.screen, "CURRENT SCORE : {}".format(self.player.current_score), HSCOREFONT, HSCORESIZE, WHITE, CSCOREPOS)
        self.draw_text(self.screen, "HIGH SCORE : {}".format(self.high_score), HSCOREFONT, HSCORESIZE, WHITE, HCSCOREPOS)
        
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.state = 'over'
                self.high_score = self.player.high_score
        
        if self.coins == None:
            self.state = 'winner'


#-------------GAMEOVER FUNCTIONS---------------------#

    def over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game_reset()
                self.state = 'playing'

    def over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "GAME OVER", INTROTEXTFONT, INTROTEXTSIZE, GREEN, INTROTEXTPOS)
        self.draw_text(self.screen, "PRESS ENTER TO PLAY", INTROTEXTFONT, INTROTEXTSIZE, BLUE, ENTERTEXTPOS)
        self.draw_text(self.screen, "HIGH SCORE : {}".format(self.high_score), HSCOREFONT, HSCORESIZE, WHITE, HSCOREPOS)
        self.over_update()

    def over_update(self):
        pygame.display.update()
    

#-----------------WIN FUNCTIONS-------------------#

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'playing'

    def win_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "YOU WIN !", INTROTEXTFONT, INTROTEXTSIZE, INTROTEXTCOLOR, INTROTEXTPOS)
        self.draw_text(self.screen, "PRESS ENTER TO PLAY AGAIN", INTROTEXTFONT, INTROTEXTSIZE, INTROTEXTCOLOR, ENTERTEXTPOS)
        pygame.win_update()

    def win_update():
        pygame.display.update()

            
                
