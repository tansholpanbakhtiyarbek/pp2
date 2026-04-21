import pygame
import random
import sys

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
GRAY = (40, 40, 40)

# ---------------- GAME RESET ----------------
def reset_game():
    snake = [(100, 100)]
    direction = (CELL, 0)
    food = spawn_food(snake)

    score = 0
    level = 1
    speed = 4

    return snake, direction, food, score, level, speed


def spawn_food(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)


def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))


# ---------------- INIT GAME ----------------
snake, direction, food, score, level, speed = reset_game()
game_over = False

# ---------------- MAIN LOOP ----------------
while True:
    screen.fill(BLACK)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ESC = quit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # RESTART KEY
            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, level, speed = reset_game()
                game_over = False

    # -------- INPUT --------
    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and direction != (CELL, 0):
            direction = (-CELL, 0)
        elif keys[pygame.K_RIGHT] and direction != (-CELL, 0):
            direction = (CELL, 0)
        elif keys[pygame.K_UP] and direction != (0, CELL):
            direction = (0, -CELL)
        elif keys[pygame.K_DOWN] and direction != (0, -CELL):
            direction = (0, CELL)

    # -------- GAME LOGIC --------
    if not game_over:
        hx, hy = snake[0]
        dx, dy = direction

        new_head = (hx + dx, hy + dy)

        # wall collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            game_over = True

        # self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            # eat food
            if new_head == food:
                score += 1
                food = spawn_food(snake)

                if score % 3 == 0:
                    level += 1
                    speed += 1
            else:
                snake.pop()

    # -------- DRAW SNAKE --------
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else (0, 140, 0)
        pygame.draw.rect(screen, color, (x, y, CELL, CELL))

    # -------- DRAW FOOD --------
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # -------- UI --------
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {level}", 10, 40)

    if game_over:
        draw_text("GAME OVER", 200, 220)
        draw_text("Press R to restart", 150, 270)
        draw_text("ESC to quit", 210, 310)

    pygame.display.flip()
    clock.tick(speed)