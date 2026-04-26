import pygame
import random
import sys
import json
import os
from db import save_result, get_personal_best, get_top_10

pygame.init()

# ===================== SCREEN SETTINGS =====================
WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 60

# ===================== COLORS =====================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
DARK_GRAY = (35, 35, 35)
GREEN = (0, 255, 0)
BODY_GREEN = (0, 180, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
BLUE = (0, 150, 255)
PURPLE = (160, 80, 255)
CYAN = (0, 230, 230)

FOOD_COLORS = {
    1: YELLOW,
    3: ORANGE,
    5: RED
}

# ===================== FONTS =====================
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 52)
small_font = pygame.font.SysFont(None, 24)


# ===================== SETTINGS JSON =====================
def load_settings():
    if not os.path.exists("settings.json"):
        settings = {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }
        save_settings(settings)
        return settings

    with open("settings.json", "r") as file:
        return json.load(file)


def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


# ===================== BUTTON =====================
def draw_button(screen, rect, text):
    pygame.draw.rect(screen, GRAY, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


# ===================== RANDOM POSITION =====================
def random_position(snake, food=None, poison=None, powerup=None, obstacles=None):
    if obstacles is None:
        obstacles = []

    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        pos = (x, y)

        blocked = pos in snake or pos in obstacles

        if food and pos == food["pos"]:
            blocked = True

        if poison and poison["active"] and pos == poison["pos"]:
            blocked = True

        if powerup and powerup["active"] and pos == powerup["pos"]:
            blocked = True

        if not blocked:
            return pos


# ===================== FOOD =====================
def spawn_food(snake, obstacles):
    value = random.choice([1, 3, 5])

    if value == 1:
        growth = 1
        lifetime = 7
    elif value == 3:
        growth = 2
        lifetime = 6
    else:
        growth = 3
        lifetime = 5

    return {
        "pos": random_position(snake, obstacles=obstacles),
        "value": value,
        "growth": growth,
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": lifetime * 1000
    }


# ===================== POISON FOOD =====================
def spawn_poison(snake, food, obstacles):
    return {
        "pos": random_position(snake, food=food, obstacles=obstacles),
        "active": True,
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 8000
    }


# ===================== POWER UP =====================
def spawn_powerup(snake, food, poison, obstacles):
    return {
        "pos": random_position(snake, food=food, poison=poison, obstacles=obstacles),
        "kind": random.choice(["speed", "slow", "shield"]),
        "active": True,
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": 8000
    }


# ===================== OBSTACLES =====================
def generate_obstacles(level, snake, food):
    obstacles = []

    if level < 3:
        return obstacles

    amount = min(level - 2, 6)

    for _ in range(amount):
        pos = random_position(snake, food=food, obstacles=obstacles)

        # Do not place obstacle too close to snake head
        hx, hy = snake[0]
        if abs(pos[0] - hx) + abs(pos[1] - hy) > CELL * 5:
            obstacles.append(pos)

    return obstacles


# ===================== DRAW GRID =====================
def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y), 1)


# ===================== MAIN MENU =====================
def main_menu(screen):
    username = ""

    play_btn = pygame.Rect(200, 230, 200, 45)
    leaderboard_btn = pygame.Rect(200, 285, 200, 45)
    settings_btn = pygame.Rect(200, 340, 200, 45)
    quit_btn = pygame.Rect(200, 395, 200, 45)

    while True:
        screen.fill(BLACK)

        title = big_font.render("SNAKE GAME", True, WHITE)
        screen.blit(title, (165, 70))

        screen.blit(font.render("Username:", True, WHITE), (200, 145))

        pygame.draw.rect(screen, WHITE, (200, 175, 200, 40), border_radius=8)
        name_text = font.render(username + "|", True, BLACK)
        screen.blit(name_text, (210, 183))

        draw_button(screen, play_btn, "Play")
        draw_button(screen, leaderboard_btn, "Leaderboard")
        draw_button(screen, settings_btn, "Settings")
        draw_button(screen, quit_btn, "Quit")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", username

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        return "play", username

                else:
                    if len(username) < 12:
                        username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos) and username.strip() != "":
                    return "play", username

                if leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard", username

                if settings_btn.collidepoint(event.pos):
                    return "settings", username

                if quit_btn.collidepoint(event.pos):
                    return "quit", username


# ===================== LEADERBOARD SCREEN =====================
def leaderboard_screen(screen):
    back_btn = pygame.Rect(220, 530, 160, 45)

    while True:
        screen.fill(BLACK)

        title = big_font.render("TOP 10", True, WHITE)
        screen.blit(title, (230, 40))

        rows = get_top_10()

        header = small_font.render("Rank   Name        Score   Level   Date", True, WHITE)
        screen.blit(header, (45, 110))

        y = 145
        for i, row in enumerate(rows):
            username, score, level, played_at = row
            date_text = str(played_at).split(".")[0]

            text = small_font.render(
                f"{i + 1:<5} {username[:10]:<10} {score:<7} {level:<6} {date_text[:10]}",
                True,
                WHITE
            )
            screen.blit(text, (45, y))
            y += 32

        draw_button(screen, back_btn, "Back")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


# ===================== SETTINGS SCREEN =====================
def settings_screen(screen):
    settings = load_settings()

    grid_btn = pygame.Rect(190, 180, 220, 45)
    sound_btn = pygame.Rect(190, 245, 220, 45)
    color_btn = pygame.Rect(190, 310, 220, 45)
    save_btn = pygame.Rect(190, 420, 220, 45)

    colors = [
        [0, 255, 0],
        [0, 150, 255],
        [255, 120, 0],
        [180, 80, 255]
    ]

    while True:
        screen.fill(BLACK)

        title = big_font.render("SETTINGS", True, WHITE)
        screen.blit(title, (190, 70))

        draw_button(screen, grid_btn, f"Grid: {settings['grid']}")
        draw_button(screen, sound_btn, f"Sound: {settings['sound']}")
        draw_button(screen, color_btn, "Change Snake Color")
        draw_button(screen, save_btn, "Save & Back")

        pygame.draw.rect(screen, settings["snake_color"], (270, 370, 60, 35), border_radius=6)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(event.pos):
                    current = settings["snake_color"]
                    index = colors.index(current) if current in colors else 0
                    settings["snake_color"] = colors[(index + 1) % len(colors)]

                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return


# ===================== GAME OVER SCREEN =====================
def game_over_screen(screen, username, score, level, personal_best):
    retry_btn = pygame.Rect(200, 350, 200, 45)
    menu_btn = pygame.Rect(200, 410, 200, 45)

    while True:
        screen.fill(BLACK)

        title = big_font.render("GAME OVER", True, RED)
        screen.blit(title, (180, 100))

        screen.blit(font.render(f"Player: {username}", True, WHITE), (200, 180))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (200, 220))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (200, 260))
        screen.blit(font.render(f"Best: {personal_best}", True, WHITE), (200, 300))

        draw_button(screen, retry_btn, "Retry")
        draw_button(screen, menu_btn, "Main Menu")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"


# ===================== GAME LOOP =====================
def game_loop(screen, username):
    clock = pygame.time.Clock()

    while True:
        settings = load_settings()
        snake_color = tuple(settings["snake_color"])
        personal_best = get_personal_best(username)

        snake = [(100, 100)]
        direction = (CELL, 0)

        score = 0
        level = 1
        speed = 5
        growth = 0

        obstacles = []
        food = spawn_food(snake, obstacles)
        poison = {"active": False}
        powerup = {"active": False}

        active_power = None
        power_end_time = 0
        shield = False

        last_level = level
        game_over = False

        while not game_over:
            clock.tick(speed)
            now = pygame.time.get_ticks()

            # ===================== EVENTS =====================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ===================== INPUT =====================
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif keys[pygame.K_RIGHT] and direction != (-CELL, 0):
                direction = (CELL, 0)
            elif keys[pygame.K_UP] and direction != (0, CELL):
                direction = (0, -CELL)
            elif keys[pygame.K_DOWN] and direction != (0, -CELL):
                direction = (0, CELL)

            # ===================== POWER-UP TIMER =====================
            if active_power in ["speed", "slow"] and now > power_end_time:
                active_power = None

            # ===================== MOVE SNAKE =====================
            hx, hy = snake[0]
            dx, dy = direction
            new_head = (hx + dx, hy + dy)

            collision = False

            # Wall collision
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                collision = True

            # Self collision
            if new_head in snake:
                collision = True

            # Obstacle collision
            if new_head in obstacles:
                collision = True

            # Shield ignores one collision
            if collision:
                if shield:
                    shield = False
                    continue
                else:
                    game_over = True
                    break

            snake.insert(0, new_head)

            # ===================== EAT NORMAL FOOD =====================
            if new_head == food["pos"]:
                score += food["value"]
                growth += food["growth"]

                food = spawn_food(snake, obstacles)

                if score % 3 == 0:
                    level += 1
                    speed += 1

            # ===================== EAT POISON =====================
            if poison.get("active") and new_head == poison["pos"]:
                for _ in range(2):
                    if len(snake) > 1:
                        snake.pop()

                poison["active"] = False

                if len(snake) <= 1:
                    game_over = True
                    break

            # ===================== EAT POWER-UP =====================
            if powerup.get("active") and new_head == powerup["pos"]:
                if powerup["kind"] == "speed":
                    active_power = "speed"
                    power_end_time = now + 5000
                    speed += 2

                elif powerup["kind"] == "slow":
                    active_power = "slow"
                    power_end_time = now + 5000
                    speed = max(3, speed - 2)

                elif powerup["kind"] == "shield":
                    shield = True

                powerup["active"] = False

            # ===================== GROWTH SYSTEM =====================
            if growth > 0:
                growth -= 1
            else:
                snake.pop()

            # ===================== FOOD TIMER =====================
            if now - food["spawn_time"] > food["lifetime"]:
                food = spawn_food(snake, obstacles)

            # ===================== POISON TIMER =====================
            if not poison.get("active") and random.randint(1, 70) == 1:
                poison = spawn_poison(snake, food, obstacles)

            if poison.get("active") and now - poison["spawn_time"] > poison["lifetime"]:
                poison["active"] = False

            # ===================== POWER-UP TIMER =====================
            if not powerup.get("active") and active_power is None and random.randint(1, 90) == 1:
                powerup = spawn_powerup(snake, food, poison, obstacles)

            if powerup.get("active") and now - powerup["spawn_time"] > powerup["lifetime"]:
                powerup["active"] = False

            # ===================== OBSTACLES BY LEVEL =====================
            if level >= 3 and level != last_level:
                obstacles = generate_obstacles(level, snake, food)
                last_level = level

            # ===================== DRAW EVERYTHING =====================
            screen.fill(BLACK)

            if settings["grid"]:
                draw_grid(screen)

            # Draw obstacles
            for ox, oy in obstacles:
                pygame.draw.rect(screen, GRAY, (ox, oy, CELL, CELL))

            # Draw snake
            for i, (x, y) in enumerate(snake):
                if i == 0:
                    color = snake_color
                else:
                    color = BODY_GREEN

                pygame.draw.rect(screen, color, (x, y, CELL, CELL))

            # Draw shield outline
            if shield:
                hx, hy = snake[0]
                pygame.draw.rect(screen, PURPLE, (hx - 4, hy - 4, CELL + 8, CELL + 8), 2)

            # Draw food
            food_color = FOOD_COLORS[food["value"]]
            pygame.draw.rect(screen, food_color, (food["pos"][0], food["pos"][1], CELL, CELL))

            # Draw poison
            if poison.get("active"):
                pygame.draw.rect(screen, DARK_RED, (poison["pos"][0], poison["pos"][1], CELL, CELL))

            # Draw power-up
            if powerup.get("active"):
                if powerup["kind"] == "speed":
                    color = CYAN
                    text = "F"
                elif powerup["kind"] == "slow":
                    color = BLUE
                    text = "S"
                else:
                    color = PURPLE
                    text = "H"

                pygame.draw.rect(screen, color, (powerup["pos"][0], powerup["pos"][1], CELL, CELL))
                label = small_font.render(text, True, WHITE)
                screen.blit(label, (powerup["pos"][0] + 4, powerup["pos"][1] + 2))

            # Draw UI
            screen.blit(small_font.render(f"Player: {username}", True, WHITE), (10, 10))
            screen.blit(small_font.render(f"Score: {score}", True, WHITE), (10, 35))
            screen.blit(small_font.render(f"Level: {level}", True, WHITE), (10, 60))
            screen.blit(small_font.render(f"Best: {personal_best}", True, WHITE), (10, 85))

            if active_power == "speed":
                left = max(0, (power_end_time - now) // 1000)
                screen.blit(small_font.render(f"Speed: {left}s", True, WHITE), (430, 10))

            if active_power == "slow":
                left = max(0, (power_end_time - now) // 1000)
                screen.blit(small_font.render(f"Slow: {left}s", True, WHITE), (430, 10))

            if shield:
                screen.blit(small_font.render("Shield: ON", True, WHITE), (430, 35))

            pygame.display.flip()

        # ===================== SAVE RESULT =====================
        save_result(username, score, level)

        updated_best = max(personal_best, score)
        result = game_over_screen(screen, username, score, level, updated_best)

        if result == "menu":
            return

        if result == "retry":
            continue