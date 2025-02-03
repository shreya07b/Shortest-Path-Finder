import pygame
import queue
import time

pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 9, 9
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Maze
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest Path Finder")

def draw_maze(maze, path=[]):
    screen.fill(WHITE)
    
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * CELL_SIZE, row * CELL_SIZE
            if maze[row][col] == "#":
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif maze[row][col] == "O":
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            elif maze[row][col] == "X":
                pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

            if (row, col) in path:
                pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    pygame.display.update()

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_neighbors(maze, row, col):
    neighbors = []
    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))
    return neighbors

def find_path(maze):
    start_pos = find_start(maze, "O")
    end_pos = find_start(maze, "X")

    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        # Stop if we reach the end
        if maze[row][col] == "X":
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

        draw_maze(maze, path)
        time.sleep(0.1)

    return []

# Main Loop
running = True
path = find_path(maze)

while running:
    draw_maze(maze, path)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
