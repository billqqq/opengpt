# Minimal Tetris game using pygame
import pygame
import random
import sys

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Screen dimensions
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
COLORS = [
    (0, 240, 240),  # I
    (0, 0, 240),    # J
    (240, 160, 0),  # L
    (240, 240, 0),  # O
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0),    # Z
]

# Tetromino shapes
SHAPES = [
    [
        ['.....',
         '..0..',
         '..0..',
         '..0..',
         '..0..'],
        ['.....',
         '0000.',
         '.....',
         '.....',
         '.....'],
    ],  # I
    [
        ['.....',
         '.0...',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..00.',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '...0.',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '.00..',
         '.....'],
    ],  # J
    [
        ['.....',
         '...0.',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '..00.',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '.0...',
         '.....'],
        ['.....',
         '.00..',
         '..0..',
         '..0..',
         '.....'],
    ],  # L
    [
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....'],
    ],  # O
    [
        ['.....',
         '..00.',
         '.00..',
         '.....',
         '.....'],
        ['.....',
         '.0..',
         '.00.',
         '..0.',
         '.....'],
    ],  # S
    [
        ['.....',
         '..0..',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '..0..',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '..0..',
         '.....'],
    ],  # T
    [
        ['.....',
         '.00..',
         '..00.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '.0...',
         '.....'],
    ],  # Z
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0


def create_grid(locked):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for (x, y), color in locked.items():
        if y >= 0:
            grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions


def valid_space(piece, grid):
    accepted = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted = [j for sub in accepted for j in sub]
    for pos in convert_shape_format(piece):
        if pos not in accepted:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for (x, y) in positions:
        if y < 0:
            return True
    return False


def clear_rows(grid, locked):
    cleared = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        if BLACK not in grid[i]:
            cleared += 1
            index = i
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
    if cleared > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                newKey = (x, y + cleared)
                locked[newKey] = locked.pop(key)
    return cleared


def get_shape():
    return Piece(GRID_WIDTH // 2 - 2, 0, random.choice(SHAPES))


def draw_grid(surface, grid):
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, SCREEN_HEIGHT))


def draw_window(surface, grid, score):
    surface.fill(BLACK)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
    draw_grid(surface, grid)
    font = pygame.font.SysFont('comicsans', 24)
    label = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(label, (10, 10))
    pygame.display.update()


def draw_text_middle(surface, text):
    font = pygame.font.SysFont('comicsans', 48)
    label = font.render(text, True, (255, 255, 255))
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, SCREEN_HEIGHT / 2 - label.get_height() / 2))
    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)

        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = COLORS[SHAPES.index(current_piece.shape)]

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = COLORS[SHAPES.index(current_piece.shape)]
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)

        if check_lost(locked_positions):
            run = False

    draw_text_middle(win, 'Game Over')
    pygame.display.update()
    pygame.time.delay(1500)
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main_loop():
    main()


if __name__ == '__main__':
    main_loop()
