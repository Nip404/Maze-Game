import mEngine as engine
import pygame
import random as rn
import sys
import time

### Used only for creation of maze
class Animator:
    sq = 30
    
    def __init__(self, w, l, sq=None):
        self.w = w
        self.l = l
        self.sq = self.sq if not isinstance(sq, int) else sq
        self.s = [w*self.sq, l*self.sq]

        pygame.init()
        self.surf = pygame.display.set_mode(self.s, 0, 32)
        pygame.display.set_caption(f"Generating Maze ({self.w}x{self.l})")

    def draw(self, maze, current):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for y,row in enumerate(maze):
            for x,cell in enumerate(row):
                pygame.draw.rect(self.surf, ((255,255,255) if not cell.visited else (173,255,47)) if not current == [x,y] else (255,0,0), [x*self.sq, y*self.sq, self.sq, self.sq], 0)

                for n,w in cell.walls.items():
                    if n == "U" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, y*self.sq), ((x+1)*self.sq, y*self.sq), 1)
                    elif n == "D" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, (y+1)*self.sq), ((x+1)*self.sq, (y+1)*self.sq), 1)
                    elif n == "L" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, y*self.sq), (x*self.sq, (y+1)*self.sq), 1)
                    elif n == "R" and w:
                        pygame.draw.line(self.surf, (0,0,0), ((x+1)*self.sq, y*self.sq), ((x+1)*self.sq, (y+1)*self.sq), 1)

        pygame.display.flip()

### Graphics superclass
class gEngine:
    sq = 30
    
    def __init__(self, maze, sq=None):
        self.w = len(maze[0])
        self.l = len(maze)
        self.maze = maze

        self.sq = self.sq if not isinstance(sq, int) else sq
        self.s = [self.w*self.sq, self.l*self.sq]

        pygame.init()
        self.surf = pygame.display.set_mode(self.s)
        self.blind = pygame.Surface(self.surf.get_size(), pygame.SRCALPHA)
        self.end = pygame.Surface(self.surf.get_size())
        self.end.set_alpha(150)
        self.h1 = pygame.font.SysFont("Tahoma", 50)
        self.h2 = pygame.font.SysFont("Tahoma", 30)

    def draw(self, endscr=False):
        for y,row in enumerate(self.maze):
            for x,cell in enumerate(row):
                pygame.draw.rect(self.surf, (255,255,255), [x*self.sq, y*self.sq, self.sq, self.sq], 0)

        for y,row in enumerate(self.maze):
            for x,cell in enumerate(row):
                for n,w in cell.walls.items():
                    if n == "U" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, y*self.sq), ((x+1)*self.sq, y*self.sq), 1)
                    elif n == "D" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, (y+1)*self.sq), ((x+1)*self.sq, (y+1)*self.sq), 1)
                    elif n == "L" and w:
                        pygame.draw.line(self.surf, (0,0,0), (x*self.sq, y*self.sq), (x*self.sq, (y+1)*self.sq), 1)
                    elif n == "R" and w:
                        pygame.draw.line(self.surf, (0,0,0), ((x+1)*self.sq, y*self.sq), ((x+1)*self.sq, (y+1)*self.sq), 1)

        pygame.draw.circle(self.surf, (0,0,255), list(map(int,((self.player[0]+0.5)*self.sq, (self.player[1]+0.5)*self.sq))), self.sq//2, 0)
        pygame.draw.circle(self.surf, (0,255,0), list(map(int,((self.dest[0]+0.5)*self.sq, (self.dest[1]+0.5)*self.sq))), self.sq//2, 0)

        if endscr:
            s1 = self.h1.render(f"Score: {self.score}(s)", True, (0,0,0))
            s2 = self.h2.render(f"Highscore: {self.highscore}(s)", True, (0,0,0))

            self.end.fill((255, 255, 255))
            self.end.blit(s1, s1.get_rect(center=[self.s[0]/2, self.s[1]*0.3]))
            self.end.blit(s2, s2.get_rect(center=[self.s[0]/2, self.s[1]*0.7]))
            self.surf.blit(self.end, (0,0))
        else:
            self.blind.fill((0,0,0,255))
            pygame.draw.circle(self.blind, (255,255,255,0), pygame.mouse.get_pos(), sum(self.surf.get_size())//8, 0)
            self.surf.blit(self.blind, (0,0))

        pygame.display.flip()

    def endscreen(self):
        self.end.fill((255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.draw(endscr=True)
            self.update_score()

class Game(gEngine):
    def __init__(self, maze):
        super().__init__(maze)

    def _init_game_vars(self):
        #coords = [[x,y] for y in range(len(self.maze)) for x in range(len(self.maze[0]))]

        #self.player = coords.pop(rn.randrange(len(coords)))
        #self.dest = coords.pop(rn.randrange(len(coords)))

        self.player = [0,0]
        self.dest = [len(self.maze[0])-1, len(self.maze)-1]

    def possible_vectors(self, player):
        possible = []

        for v in [[-1,0], [0,-1], [1,0], [0,1]]:
            if (v[0] > 0 and not self.maze[player[1]][player[0]].walls["R"]) or\
               (v[0] < 0 and not self.maze[player[1]][player[0]].walls["L"]) or\
               (v[1] > 0 and not self.maze[player[1]][player[0]].walls["D"]) or\
               (v[1] < 0 and not self.maze[player[1]][player[0]].walls["U"]):
                possible.append(v)

        return possible

    def update_score(self):
        pygame.display.set_caption(f"Maze Game | Highscore: {self.highscore}(s) | Score: {self.score}(s)")

    def _play(self):
        self._init_game_vars()
        t0 = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    move = True
                    
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        vector = [0, -1]

                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        vector = [0, 1]

                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        vector = [-1, 0]

                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        vector = [1, 0]

                    else:
                        move = False
                        
                    if move and vector in self.possible_vectors(self.player):
                        self.player[0] += vector[0]
                        self.player[1] += vector[1]

            self.score = int(time.time() - t0)
            self.draw()
            self.update_score()

            if self.player == self.dest:
                if self.score < self.highscore:
                    self.highscore = self.score

                return

    def play(self, make_new_maze=True, animate_creation=False):
        self.highscore = 0

        while True:
            self._play()
            self.endscreen()

            if make_new_maze:
                self.__init__(engine.create_maze(len(self.maze[0]), len(self.maze), animate=animate_creation))
