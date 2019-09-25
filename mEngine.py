from mGameEngine import Animator
import random as rn
import itertools

def create_maze(length, width, sq=None, animate=None):
    return Maze(length, width, sq=sq, animate=animate).generate()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.visited = False
        self.walls = {
            "U": True,
            "D": True,
            "L": True,
            "R": True
        }

class Maze:
    def __init__(self, length, width, animate=False, sq=None): # implement options for different algorithms
        self.length = length
        self.width = width

        self.maze = [[Cell(x, y) for x in range(self.width)] for y in range(self.length)]

        self.animate = bool(animate)
        if self.animate:
            self.graphics = Animator(self.width, self.length, sq)

    def any_unvisited(self):
        return any(any(not c.visited for c in row) for row in self.maze)

    def get_neighbours(self, current):
        #neighbours = list(itertools.combinations_with_replacement([-1,0,1],2))
        neighbours = [(-1,0),(0,-1),(1,0),(0,1)]
        return list(filter(lambda i: (i[0] or i[1]) and (0 <= i[0]+current[0] < self.width and 0 <= i[1]+current[1] < self.length) and (not self.maze[i[1]+current[1]][i[0]+current[0]].visited), set(neighbours + [n[::-1] for n in neighbours])))

    def remove_wall(self, a, b):
        if a[0] > b[0]:
            self.maze[a[1]][a[0]].walls["L"] = False
            self.maze[b[1]][b[0]].walls["R"] = False
        elif a[0] < b[0]:
            self.maze[a[1]][a[0]].walls["R"] = False
            self.maze[b[1]][b[0]].walls["L"] = False
        if a[1] > b[1]:
            self.maze[a[1]][a[0]].walls["U"] = False
            self.maze[b[1]][b[0]].walls["D"] = False
        elif a[1] < b[1]:
            self.maze[a[1]][a[0]].walls["D"] = False
            self.maze[b[1]][b[0]].walls["U"] = False

    def generate(self): # recursive backtracker
        stack = []
        cell = [0, 0]

        while self.any_unvisited():
            self.maze[cell[1]][cell[0]].visited = True
            neighbours = self.get_neighbours(cell)

            if len(neighbours):
                neighbour = rn.choice(neighbours)
                neighbour = [cell[i] + neighbour[i] for i in range(2)]
                stack.append(cell)
                self.remove_wall(cell, neighbour)
                cell = neighbour[:]
                
            elif len(stack):
                cell = stack.pop()

            if self.animate:
                self.graphics.draw(self.maze, cell)

        return self.maze
