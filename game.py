import pygame as pg
from setting import *
import heapq
from random import randint

pg.init()
pg.display.set_caption('Ghaba')
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pg.time.Clock()
introclock = pg.time.Clock()
running = True
start, end = None, None
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
window = 'Intro'

# Game Elements
tiles = [pg.image.load('Tiles/1.png'), pg.image.load('Tiles/2.png')]
corner = [pg.image.load('Tiles/top.png').convert_alpha(),
           pg.image.load('Tiles/bottom.png').convert_alpha(),
           pg.image.load('Tiles/left.png').convert_alpha(),
           pg.image.load('Tiles/right.png').convert_alpha()
           ]
logo = pg.image.load('assets/logo.png').convert_alpha()
logo = pg.transform.rotozoom(logo, 0, 0.6)
logo_rect = logo.get_rect(center= (WINDOW_SIZE/2, 170))
start_b = pg.image.load('assets/start.png').convert_alpha()
restart_b = pg.image.load('assets/restart.png').convert_alpha()
start_rect = start_b.get_rect(center = (WINDOW_SIZE/2, 400))
background = [pg.image.load('assets/1.png').convert(), pg.image.load('assets/2.png').convert(), pg.image.load('assets/3.png').convert()]
stone = pg.image.load('assets/stone.png')
p_front = [
    pg.image.load('assets/front-1.png'),
    pg.image.load('assets/front-2.png'),
    pg.image.load('assets/front-3.png'),
    pg.image.load('assets/front-4.png')
]

p_back = [
    pg.image.load('assets/back-1.png'),
    pg.image.load('assets/back-2.png'),
    pg.image.load('assets/back-3.png'),
    pg.image.load('assets/back-4.png')
]

p_left = [
    pg.image.load('assets/left-1.png'),
    pg.image.load('assets/left-2.png'),
    pg.image.load('assets/left-3.png'),
    pg.image.load('assets/left-4.png')
]

p_right = [
    pg.image.load('assets/right-1.png'),
    pg.image.load('assets/right-2.png'),
    pg.image.load('assets/right-3.png'),
    pg.image.load('assets/right-4.png')
]

decorations = [
    pg.image.load('Tiles/d-1.png'),
    pg.image.load('Tiles/d-2.png'),
    pg.image.load('Tiles/d-3.png'),
]

p_rect = p_front[0].get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
flag = pg.image.load('assets/flag.png')
choose = pg.image.load('assets/choose.png')
choose_rect = choose.get_rect(center= (WINDOW_SIZE/2, WINDOW_SIZE/2))

# Algorithm buttons
bfs = pg.image.load('assets/bfs.png').convert_alpha()
dfs = pg.image.load('assets/dfs.png').convert_alpha()
ucs = pg.image.load('assets/ucs.png').convert_alpha()
astar_b = pg.image.load('assets/a-star.png').convert_alpha()
greedy = pg.image.load('assets/greedy.png').convert_alpha()

align_left = 100
align_right = 500
gap = 100
bfs_rect = bfs.get_rect(center=(align_left, 2*gap))
dfs_rect = dfs.get_rect(center=(align_left, 4*gap))
ucs_rect = ucs.get_rect(center=(WINDOW_SIZE/2, 5*gap))
astar_rect = astar_b.get_rect(center=(align_right, 2*gap))
greedy_rect = greedy.get_rect(center= (align_right, 4*gap))
nopath = pg.image.load('assets/nopath.png')
c_start = pg.image.load('assets/c_start.png')
c_end = pg.image.load('assets/c_end.png')
c_rect = c_start.get_rect(center= (WINDOW_SIZE/2, 500))


# Sounds
noise = pg.mixer.Sound('sfx/noise.mp3')
noise.play(-1)
click = pg.mixer.Sound('sfx/click.mp3')
win = pg.mixer.Sound('sfx/win.mp3')
walk = pg.mixer.Sound('sfx/walk.mp3')

# Additional Variables
frame = 0
p_frame = 0
index = 0
played = False


# GUI Funtions

def drawbg():
        global frame
        if frame == 3: frame = 0
        screen.blit(background[frame], (0,0))
        frame += 1

def corners(x, y):
    global MAZE
    # Right
    if MAZE[y][x+1] != 1:
        screen.blit(corner[3], (x * Total, y * Total))
    # Left
    if MAZE[y][x-1] != 1:
        screen.blit(corner[2], (x * Total, y * Total))
    # Bottom
    if MAZE[y+1][x] != 1:
        screen.blit(corner[1], (x * Total, y * Total))
    # Top
    if MAZE[y-1][x] != 1:
        screen.blit(corner[0], (x * Total, y * Total))

def player_animation(path, index, frame):
    global p_front
    global p_left
    global p_back
    global p_right

    surface = p_front[0]

    if index < len(path) - 1:
        x = path[index][0]
        xx = path[index+1][0]
        y = path[index][1]
        yy = path[index+1][1]

        if yy > y:
            surface = p_front[frame]
        elif yy < y:
            surface = p_back[frame]
        elif xx > x:
            surface = p_right[frame]
        else:
            surface = p_left[frame]

    return surface


# Maze functions

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    heap = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    found = 0
 
    while heap:
        current_cost, current_pos = heapq.heappop(heap)
 
        if current_pos == end:
            found = 1
            break
 
        for next_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_pos[0] + next_pos[0], current_pos[1] + next_pos[1])
 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[1]][neighbor[0]]:
                new_cost = cost[current_pos] + 1
 
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    priority = new_cost + heuristic(end, neighbor)
                    heapq.heappush(heap, (priority, neighbor))
                    came_from[neighbor] = current_pos
 
    path = []
    current = end
 
    #no path
    if found == 0:return path
 
    while current != start:
        path.append(current)
        current = came_from[current]
 
    path.append(start)
    return path[::-1]
 
def BFS(maze, start, end):
    queue = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    found = 0
 
    while queue:
        current_cost, current_pos = queue.pop(0)
 
        if current_pos == end:
            found = 1
            break
 
        for next_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_pos[0] + next_pos[0], current_pos[1] + next_pos[1])
 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[1]][neighbor[0]]:
                new_cost = cost[current_pos] + 1
 
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    queue.append((new_cost,neighbor))
                    came_from[neighbor] = current_pos
    path = []
    current = end
 
    #no path
    if found == 0:return path
 
    while current != start:
        path.append(current)
        current = came_from[current]
 
    path.append(start)
    return path[::-1]
 
def UCS(maze, start, end):
    heap = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    found = 0
 
    while heap:
        current_cost, current_pos = heapq.heappop(heap)
 
        if current_pos == end:
            found = 1
            break
 
        for next_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_pos[0] + next_pos[0], current_pos[1] + next_pos[1])
 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[1]][neighbor[0]]:
                new_cost = cost[current_pos] + 1
 
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    came_from[neighbor] = current_pos
 
    path = []
    current = end
 
    #no path
    if found == 0:return path
 
    while current != start:
        path.append(current)
        current = came_from[current]
 
    path.append(start)
    return path[::-1]
 
def DFS(maze, start, end):
    queue = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    found = 0
 
    while queue:
        current_cost, current_pos = queue.pop(-1)
 
        if current_pos == end:
            found = 1
            break
 
        for next_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_pos[0] + next_pos[0], current_pos[1] + next_pos[1])
 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[1]][neighbor[0]]:
                new_cost = cost[current_pos] + 1
 
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    queue.append((new_cost,neighbor))
                    came_from[neighbor] = current_pos
    path = []
    current = end
 
    #no path
    if found == 0:return path
 
    while current != start:
        path.append(current)
        current = came_from[current]
 
    path.append(start)
    return path[::-1]
 
def greedy_a(maze, start, end):
    heap = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    found = 0
 
    while heap:
        current_cost, current_pos = heapq.heappop(heap)
 
        if current_pos == end:
            found = 1
            break
 
        for next_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_pos[0] + next_pos[0], current_pos[1] + next_pos[1])
 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[1]][neighbor[0]]:
                new_cost = cost[current_pos] + heuristic(end,neighbor)
 
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    came_from[neighbor] = current_pos
 
    path = []
    current = end
 
    #no path
    if found == 0:return path
 
    while current != start:
        path.append(current)
        current = came_from[current]
 
    path.append(start)
    return path[::-1]

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if window == 'Intro' or played == True:
            if start_rect.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                if event.type == pg.MOUSEBUTTONDOWN:
                    click.play()
                    if window == 'Intro': window = 'Choose'
                    elif window == 'Select': window = 'Intro'
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        elif window == 'Select':
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                xx = pos[0] // Total
                yy = pos[1] // Total
                if not start and MAZE[yy][xx]:
                    start = (xx, yy)
                    click.play()
                elif not end and MAZE[yy][xx] and start != (xx, yy):
                    end = (xx, yy)
                    click.play()
                elif start == (xx, yy) and end == None:
                    start = None
                # elif start == (xx, yy):
                #     start = None
        elif window == 'Choose':
            if event.type == pg.MOUSEBUTTONDOWN:
                if bfs_rect.collidepoint(pg.mouse.get_pos()):
                    click.play()
                    algorithm = 'bfs'
                    window = 'Select'

                elif dfs_rect.collidepoint(pg.mouse.get_pos()):
                    click.play()
                    algorithm = 'dfs'
                    window = 'Select'

                elif astar_rect.collidepoint(pg.mouse.get_pos()):
                    click.play()
                    algorithm = 'astar'
                    window = 'Select'

                elif greedy_rect.collidepoint(pg.mouse.get_pos()):
                    click.play()
                    algorithm = 'greedy'
                    window = 'Select'
                
                elif ucs_rect.collidepoint(pg.mouse.get_pos()):
                    click.play()
                    algorithm = 'ucs'
                    window = 'Select'
                print(algorithm)


    if window == 'Intro':
        p_frame = 0
        index = 0
        played = False
        start = None
        end = None
        algorithm = None
        walking = False
        MAZE = create()
        decoration_tiles = decorate(MAZE)
        drawbg()
        screen.blit(logo, logo_rect)
        screen.blit(p_front[0], p_rect)
        screen.blit(start_b, start_rect)
        pg.display.update()
        introclock.tick(5)
    
    elif window == 'Choose':
        drawbg()
        screen.blit(choose, choose_rect)
        screen.blit(bfs, bfs_rect)
        screen.blit(dfs, dfs_rect)
        screen.blit(ucs, ucs_rect)
        screen.blit(astar_b, astar_rect)
        screen.blit(greedy, greedy_rect)

        pg.display.update()
        introclock.tick(5)

    elif window == 'Select':

        for y in range(len(MAZE)):
            for x in range(len(MAZE)):
                if MAZE[y][x] == 1:
                    screen.blit(tiles[1], (x * Total, y * Total, SQUARE_SIZE, SQUARE_SIZE))
                elif not MAZE[y][x]:
                    screen.blit(tiles[0], (x * Total, y * Total, SQUARE_SIZE, SQUARE_SIZE))               
                else:
                    screen.blit(tiles[2], (x * Total, y * Total, SQUARE_SIZE, SQUARE_SIZE))
                           
        for y in range(1, len(MAZE)-1):
            for x in range(1, len(MAZE)-1):
                if MAZE[y][x] == 1:
                    corners(x, y)

        for y in range(len(decoration_tiles)):
            for x in range(len(decoration_tiles)):
                if decoration_tiles[y][x]:
                    screen.blit(decorations[decoration_tiles[y][x] - 1], (x * Total, y * Total))
        
        if start and end:
            if algorithm == 'astar': path = a_star(MAZE, start, end)
            elif algorithm == 'greedy': path = greedy_a(MAZE, start, end)
            elif algorithm == 'bfs': path = BFS(MAZE, start, end)
            elif algorithm == 'dfs': path = DFS(MAZE, start, end)
            else: path = UCS(MAZE, start, end)

            if len(path)>0:  
                screen.blit(player_animation(path, index, p_frame), (path[index][0] * Total, path[index][1] * Total - 40, SQUARE_SIZE, SQUARE_SIZE))
                if not walking: walk.play(-1)
                walking = True
                if index < len(path) - 1:
                    index += 1
                    p_frame += 1
                    if p_frame == 4: p_frame = 0
                else:
                    p_frame = 0
                    if not played:
                        walk.stop()
                        win.play()
                        played = True
                    screen.blit(restart_b, start_rect)
            else:
                screen.blit(nopath, c_rect)
                screen.blit(restart_b, start_rect)
                played = True
        if start == None and end == None:
            screen.blit(c_start, c_rect)
        elif start and end == None:
            screen.blit(c_end, c_rect)
        
        if start:
            screen.blit(flag, (start[0] * Total, start[1] * Total, SQUARE_SIZE, SQUARE_SIZE))
        if end:
            screen.blit(flag, (end[0] * Total, end[1] * Total, SQUARE_SIZE, SQUARE_SIZE))
 
        pg.display.update()
        clock.tick(5)
pg.quit()
