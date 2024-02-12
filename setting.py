import random
WINDOW_SIZE = 600
SQUARE_SIZE = 50
Margin = 0
Total = SQUARE_SIZE + Margin
choices = [1,1,1,1,1,0,0]
decoration_choices = [1, 1, 1, 2, 3, 0, 1, 1, 0, 0, 1]
def create():
    MAZE = []

    for i in range(WINDOW_SIZE//Total):
        x = []
        for j in range(WINDOW_SIZE//Total):
            if i == 0 or j == 0 or i == WINDOW_SIZE//Total-1 or j == WINDOW_SIZE//Total-1:
                x.append(0)
            else: x.append(random.choice(choices))
        MAZE.append(x)
    return MAZE

def decorate(MAZE):
    decoration_tiles = []

    for y in range(len(MAZE)):
        cols = []
        for x in range(len(MAZE)):
            if MAZE[y][x] == 0: cols.append(random.choice(decoration_choices))
            else: cols.append(0)
        decoration_tiles.append(cols)
    
    return decoration_tiles