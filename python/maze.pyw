import pygame
import random

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 60

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Maze")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PLAYER_RADIUS = CELL_SIZE // 4

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = [True, True, True, True]

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(win, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls[0]:
            pygame.draw.line(win, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(win, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:
            pygame.draw.line(win, BLACK, (x, y + CELL_SIZE), (x, y), 2)

def index(row, col):
    if row < 0 or col < 0 or row >= ROWS or col >= COLS:
        return None
    return row * COLS + col

def remove_walls(a, b):
    dx = a.col - b.col
    if dx == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif dx == -1:
        a.walls[1] = False
        b.walls[3] = False

    dy = a.row - b.row
    if dy == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif dy == -1:
        a.walls[2] = False
        b.walls[0] = False

def generate_maze():
    global grid, maze_generated
    grid = [Cell(row, col) for row in range(ROWS) for col in range(COLS)]
    maze_generated = False

    start_cell = grid[0]
    start_cell.visited = True
    walls = []

    for direction in range(4):
        neighbor = get_neighbor(start_cell, direction)
        if neighbor:
            walls.append((start_cell, neighbor))

    while walls:
        cell, neighbor = random.choice(walls)
        walls.remove((cell, neighbor))

        if not neighbor.visited:
            remove_walls(cell, neighbor)
            neighbor.visited = True

            for direction in range(4):
                next_neighbor = get_neighbor(neighbor, direction)
                if next_neighbor and not next_neighbor.visited:
                    walls.append((neighbor, next_neighbor))

    maze_generated = True

def get_neighbor(cell, direction):
    row, col = cell.row, cell.col
    idx = index(row - 1, col) if direction == 0 else index(row, col + 1) if direction == 1 else index(row + 1, col) if direction == 2 else index(row, col - 1)
    return grid[idx] if idx is not None else None

def draw_loading_screen():
    win.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Generating Maze...", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(text, text_rect)
    pygame.display.flip()

draw_loading_screen()
generate_maze()

player_pos = [0, 0]
exit_pos = [ROWS - 1, COLS - 1]

running = True
while running:
    clock.tick(FPS)
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_pos[1] > 0:
                if not grid[player_pos[0] * COLS + player_pos[1]].walls[3]:
                    player_pos[1] -= 1
            if event.key == pygame.K_RIGHT and player_pos[1] < COLS - 1:
                if not grid[player_pos[0] * COLS + player_pos[1]].walls[1]:
                    player_pos[1] += 1
            if event.key == pygame.K_UP and player_pos[0] > 0:
                if not grid[player_pos[0] * COLS + player_pos[1]].walls[0]:
                    player_pos[0] -= 1
            if event.key == pygame.K_DOWN and player_pos[0] < ROWS - 1:
                if not grid[player_pos[0] * COLS + player_pos[1]].walls[2]:
                    player_pos[0] += 1

    for cell in grid:
        cell.draw(win)

    pygame.draw.circle(win, RED, (player_pos[1] * CELL_SIZE + CELL_SIZE // 2, player_pos[0] * CELL_SIZE + CELL_SIZE // 2), PLAYER_RADIUS)
    pygame.draw.rect(win, GREEN, (exit_pos[1] * CELL_SIZE, exit_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if player_pos == exit_pos:
        draw_loading_screen()
        generate_maze()
        player_pos = [0, 0]

    pygame.display.flip()

pygame.quit()
