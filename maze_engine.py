import pygame
import sys
import random

class Maze:
    def __init__(self,resolution,surf):
        self.surf = surf
        self.r = resolution
        self.drawmode = False

    def generate(self):
        self.grid = [[{"visited":False,"pos":[i,j],"walls":{"up":True,"down":True,"left":True,"right":True}} for i in range(self.r[0])] for j in range(self.r[1])]
        
        cell = [0,0]
        stack = []
        while any(any(not item["visited"] for item in row) for row in self.grid):
            self.grid[cell[0]][cell[1]]["visited"] = True

            if self.check_neighbours(cell):
                new = random.choice(self.neighbours)
                stack.append(cell)

                self.remove_wall(cell,new)
                cell = new[:]
                
            else:
                cell = stack.pop(-1)

            self.tmpcell = cell

            self.animate_generation()

    def animate_generation(self):
        self.events(**{str(pygame.KEYDOWN):self.generate,str(pygame.MOUSEBUTTONDOWN):lambda: setattr(self,"drawmode",not self.drawmode)})
        self.draw()

        pygame.display.flip()

    def check_neighbours(self,current):
        self.neighbours = [
        [current[0]-1,current[1]],
        [current[0],current[1]-1],
        [current[0]+1,current[1]],
        [current[0],current[1]+1]]

        self.neighbours = [i for i in self.neighbours if not any((e < 0 or e >= self.r[p]) for p,e in enumerate(i))]
        self.neighbours = [i for i in self.neighbours if not self.grid[i[0]][i[1]]["visited"]]
        
        return True if self.neighbours else False

    def remove_wall(self,a,b):
        if b[1] > a[1]:
            self.grid[a[0]][a[1]]["walls"]["right"] = False
            self.grid[b[0]][b[1]]["walls"]["left"] = False
        if b[1] < a[1]:
            self.grid[a[0]][a[1]]["walls"]["left"] = False
            self.grid[b[0]][b[1]]["walls"]["right"] = False

        if b[0] > a[0]:
            self.grid[a[0]][a[1]]["walls"]["down"] = False
            self.grid[b[0]][b[1]]["walls"]["up"] = False
        if b[0] < a[0]:
            self.grid[a[0]][a[1]]["walls"]["up"] = False
            self.grid[b[0]][b[1]]["walls"]["down"] = False

    def events(self,**custom_events):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            else:
                for user_event,function in custom_events.items():
                    if event.type == int(user_event):
                        try:
                            function()
                        except:
                            pass
                
    def draw(self):
        self.surf.fill((0,0,0))

        gapx = self.surf.get_width()/self.r[0]
        gapy = self.surf.get_height()/self.r[1]

        for row in self.grid:
            for item in row:
                if self.drawmode:
                    pygame.draw.rect(self.surf,(255,255,255),(item["pos"][0]*gapx,item["pos"][1]*gapy,gapx,gapy),0)
                else:
                    pygame.draw.rect(self.surf,((0,0,255) if item["pos"][::-1] == self.tmpcell else ((0,255,0) if self.grid[item["pos"][1]][item["pos"][0]]["visited"] else (255,255,255))),(item["pos"][0]*gapx,item["pos"][1]*gapy,gapx,gapy),0)

                if all(t for t in item["walls"].values()):
                    continue
                
                if item["walls"]["up"]:
                    pygame.draw.line(self.surf,(0,0,0),(item["pos"][0]*gapx,item["pos"][1]*gapy),(item["pos"][0]*gapx+gapx,item["pos"][1]*gapy),2)
                if item["walls"]["down"]:
                    pygame.draw.line(self.surf,(0,0,0),(item["pos"][0]*gapx,item["pos"][1]*gapy+gapy),(item["pos"][0]*gapx+gapx,item["pos"][1]*gapy+gapy),2)
                if item["walls"]["left"]:
                    pygame.draw.line(self.surf,(0,0,0),(item["pos"][0]*gapx,item["pos"][1]*gapy),(item["pos"][0]*gapx,item["pos"][1]*gapy+gapy),2)
                if item["walls"]["right"]:
                    pygame.draw.line(self.surf,(0,0,0),(item["pos"][0]*gapx+gapx,item["pos"][1]*gapy),(item["pos"][0]*gapx+gapx,item["pos"][1]*gapy+gapy),2)
