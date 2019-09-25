from mEngine import create_maze
from mGameEngine import Game

def main():
    maze = create_maze(25, 25, animate=True)
    game = Game(maze)
    game.play(animate_creation=True)

if __name__ == "__main__":
    main()
