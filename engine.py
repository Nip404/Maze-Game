import pygame
import random
import sys

_overlap = True

class Board:
    def __init__(self,surf,resolution):
        self.resolution = resolution
        self.surf = surf
        self.board = [[0 for _ in range(resolution[1])] for _ in range(resolution[0])]

        self.square_size = int(self.surf.get_width()/self.resolution[0])
        
    def generate(self,mode=None,density=1):
        # 0 = random, density (specific to mode=0) used for: randint(0,density) == 0
        # 1 = input

        if mode is None:
            return

        if mode == 0:
            self.board = [[1 if not random.randint(0,density) else 0 for _ in range(self.resolution[1])] for _ in range(self.resolution[0])]
        elif mode == 1:
            self.input_config()

    def input_config(self):
        self.board = [[0 for _ in range(self.resolution[1])] for _ in range(self.resolution[0])]
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.board[int(pygame.mouse.get_pos()[1]/self.square_size)][int(pygame.mouse.get_pos()[0]/self.square_size)] = 1 - self.board[int(pygame.mouse.get_pos()[1]/self.square_size)][int(pygame.mouse.get_pos()[0]/self.square_size)]

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            if pygame.mouse.get_pressed()[2]:
                self.board[int(pygame.mouse.get_pos()[1]/self.square_size)][int(pygame.mouse.get_pos()[0]/self.square_size)] = 1 - self.board[int(pygame.mouse.get_pos()[1]/self.square_size)][int(pygame.mouse.get_pos()[0]/self.square_size)]

            self.draw()

            pygame.display.flip()

    def neighbours(self,pos):
        return sum(self.board[neighbour[1]][neighbour[0]] for neighbour in [p for p in [[pos[0]-1,pos[1]-1],[pos[0],pos[1]-1],[pos[0]+1,pos[1]-1],[pos[0]-1,pos[1]],[pos[0]+1,pos[1]],[pos[0]-1,pos[1]+1],[pos[0],pos[1]+1],[pos[0]+1,pos[1]+1]] if all(i >= 0 and p[q] < [len(self.board[0]),len(self.board)][q] for q,i in enumerate(p))]) if not _overlap else sum(self.board[neighbour[1]][neighbour[0]] for neighbour in [[p[0] if p[0] < len(self.board[0]) else p[0]-len(self.board[0]),p[1] if p[1] < len(self.board) else p[1]-len(self.board)] for p in [[pos[0]-1,pos[1]-1],[pos[0],pos[1]-1],[pos[0]+1,pos[1]-1],[pos[0]-1,pos[1]],[pos[0]+1,pos[1]],[pos[0]-1,pos[1]+1],[pos[0],pos[1]+1],[pos[0]+1,pos[1]+1]]])

    def advance(self):
        self.board = [[1 if ((self.board[y][x] and self.neighbours([x,y]) in [2,3]) or (not self.board[y][x] and self.neighbours([x,y]) == 3)) else 0 for x in range(len(self.board[0]))] for y in range(len(self.board))]

    def draw(self):
        for y,row in enumerate(self.board):
            for x,item in enumerate(row):
                pygame.draw.rect(self.surf,[255]*3 if item else [0]*3,[x*self.square_size,y*self.square_size,self.square_size,self.square_size],0)
