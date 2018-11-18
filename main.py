import engine
import pygame
import sys

s = [500,500]
res = [50,50]

pygame.init()
screen = pygame.display.set_mode(s,0,32)
clock = pygame.time.Clock()
pygame.display.set_caption("Conway's Game of Life")

def menu():
    h1 = pygame.font.SysFont("Garamond MS",40)
    
    box1 = pygame.Rect(100,100,300,100)
    box2 = pygame.Rect(100,300,300,100)

    txt1 = h1.render("Generate Random",True,(0,0,0))
    txt2 = h1.render("Custom",True,(0,0,0))

    onHover = (100,250,20)

    while True:
        mouse = pygame.Rect([i-1 for i in pygame.mouse.get_pos()],[2,2])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.colliderect(box1):
                    return 0

                elif mouse.colliderect(box2):
                    return 1

        screen.fill((255,255,255))
        pygame.draw.rect(screen,(255,255,255) if not mouse.colliderect(box1) else onHover,box1,0)
        pygame.draw.rect(screen,(255,255,255) if not mouse.colliderect(box2) else onHover,box2,0)
        pygame.draw.rect(screen,(0,0,0),box1,1)
        pygame.draw.rect(screen,(0,0,0),box2,1)
        screen.blit(txt1,txt1.get_rect(center=box1.center))
        screen.blit(txt2,txt2.get_rect(center=box2.center))

        pygame.display.flip()

def main():
    board = engine.Board(screen,res)
    board.generate(menu())

    paused = False

    while True:
        clock.tick(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_r:
                    board.generate(menu())
                    
        if not paused:
            board.draw()
            board.advance()

        pygame.display.flip()

if __name__ == "__main__":
    main()
