import pygame
import random
import sys
import time

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

HEAD_COLOR = (0, 255, 0)
BODY_COLOR = (0, 180, 0)

FOOD_COLORS = {
    1: (255, 255, 0),   # yellow
    3: (255, 140, 0),   # orange
    5: (220, 0, 0)      # red
}

# ---------------- RESET ----------------
def reset_game():
    snake = [(100, 100)]
    direction = (CELL, 0)

    food = spawn_food(snake)

    score = 0
    level = 1
    speed = 4

    growth = 0  # pending growth

    return snake, direction, food, score, level, speed, growth


# ---------------- FOOD ----------------
def spawn_food(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            value = random.choice([1, 3, 5])

            # lifetime rules
            if value == 5:
                lifetime = 5
            else:
                lifetime = 7

            # growth mapping (IMPORTANT)
            if value == 1:
                growth_value = 1
            elif value == 3:
                growth_value = 2
            else:
                growth_value = 3

            return {
                "pos": (x, y),
                "value": value,
                "growth": growth_value,
                "time": time.time(),
                "lifetime": lifetime
            }


# ---------------- TEXT ----------------
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))


# ---------------- INIT ----------------
snake, direction, food, score, level, speed, growth = reset_game()
game_over = False


# ---------------- MAIN LOOP ----------------
while True:
    screen.fill(BLACK)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, level, speed, growth = reset_game()
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

            # -------- EAT FOOD --------
            if new_head == food["pos"]:
                score += food["value"]          # points
                growth += food["growth"]        # size growth

                food = spawn_food(snake)

                # level system
                if score % 3 == 0:
                    level += 1
                    speed += 1

            # -------- GROWTH SYSTEM --------
            if growth > 0:
                growth -= 1
            else:
                snake.pop()

        # -------- FOOD TIMER --------
        if time.time() - food["time"] > food["lifetime"]:
            food = spawn_food(snake)

    # -------- DRAW SNAKE --------
    for i, (x, y) in enumerate(snake):
        color = HEAD_COLOR if i == 0 else BODY_COLOR
        pygame.draw.rect(screen, color, (x, y, CELL, CELL))

    # -------- DRAW FOOD --------
    color = FOOD_COLORS[food["value"]]
    pygame.draw.rect(screen, color, (food["pos"][0], food["pos"][1], CELL, CELL))

    # -------- UI --------
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {level}", 10, 40)

    if game_over:
        draw_text("GAME OVER", 200, 220)
        draw_text("Press R to restart", 150, 270)
        draw_text("ESC to quit", 210, 310)

    pygame.display.flip()
    clock.tick(speed)