# Recursive backtracker + a*

from maze_engine import Maze
import pygame
import random
import math
import sys

s = [800,800]

pygame.init()
screen = pygame.display.set_mode(s,0,32)
pygame.display.set_caption("Maze by NIP")
clock = pygame.time.Clock()

maze_res = [50,50]

def main():
    m = Maze(maze_res,screen)
    m.generate()

    while True:
        m.draw()
        m.events(**{str(pygame.KEYDOWN):m.generate,str(pygame.MOUSEBUTTONDOWN):lambda: setattr(m,"drawmode",not m.drawmode)})

        pygame.display.flip()

if __name__ == "__main__":
    main()
