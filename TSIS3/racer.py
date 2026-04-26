import pygame
import random
import sys
from persistence import save_score, load_settings

pygame.init()

# ===================== SCREEN SETTINGS =====================
WIDTH, HEIGHT = 400, 600
FPS = 60

# ===================== ROAD SETTINGS =====================
ROAD_LEFT = 80
ROAD_RIGHT = 320
LANES = [105, 180, 255]

# ===================== COLORS =====================
GREEN = (0, 180, 0)
GRAY = (110, 110, 110)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ENEMY_COLOR = (220, 60, 60)
OIL_COLOR = (30, 30, 30)
BARRIER_COLOR = (160, 80, 20)

NITRO_COLOR = (0, 220, 255)
SHIELD_COLOR = (120, 80, 255)
REPAIR_COLOR = (0, 220, 80)

COIN_COLORS = {
    1: (200, 200, 0),
    3: (255, 215, 0),
    5: (255, 140, 0)
}

# ===================== FONTS =====================
font = pygame.font.SysFont("Verdana", 18)
big_font = pygame.font.SysFont("Verdana", 34)


# ===================== DRAW CAR =====================
# Draws a car shape instead of a simple rectangle
def draw_car(surface, rect, color):
    pygame.draw.rect(surface, color, rect, border_radius=8)

    # Window
    pygame.draw.rect(
        surface,
        BLACK,
        (rect.x + 5, rect.y + 8, rect.width - 10, 15),
        border_radius=4
    )

    # Wheels / details
    pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.y + 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + rect.width - 8, rect.y + 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.y + rect.height - 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + rect.width - 8, rect.y + rect.height - 10), 5)


# ===================== PLAYER =====================
# Player car controlled by left and right arrows
class Player:
    def __init__(self, color):
        self.rect = pygame.Rect(180, 500, 40, 70)
        self.color = color
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= 6

        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += 6

    def draw(self, screen):
        draw_car(screen, self.rect, self.color)

        # Draw shield circle if shield is active
        if self.shield:
            pygame.draw.circle(screen, SHIELD_COLOR, self.rect.center, 45, 3)


# ===================== ENEMY =====================
# Traffic car that moves downward
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 40, 70)
        self.reset()

    def reset(self):
        # Spawn enemy in a random lane above the screen
        lane = random.choice(LANES)
        self.rect.x = lane
        self.rect.y = random.randint(-1000, -300)

    def move(self, speed):
        self.rect.y += speed

        # Respawn when enemy leaves the screen
        if self.rect.top > HEIGHT:
            self.reset()

    def draw(self, screen):
        draw_car(screen, self.rect, ENEMY_COLOR)


# ===================== COIN =====================
# Weighted coins from Practice 11
class Coin:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.active = False
        self.timer = random.randint(40, 120)
        self.value = 1

    def spawn(self, blocked_rects):
        # Try to spawn coin without overlapping enemies or obstacles
        for _ in range(50):
            lane = random.choice(LANES)
            self.rect.x = lane + 8
            self.rect.y = random.randint(-400, -50)

            if not any(self.rect.colliderect(r) for r in blocked_rects):
                break

        # Coin has different weights
        self.value = random.choice([1, 3, 5])
        self.active = True

    def update(self, speed, blocked_rects):
        # Coin appears after a timer
        if not self.active:
            self.timer -= 1

            if self.timer <= 0:
                self.spawn(blocked_rects)

            return

        self.rect.y += speed

        # Coin disappears after leaving the screen
        if self.rect.top > HEIGHT:
            self.active = False
            self.timer = random.randint(40, 120)

    def draw(self, screen):
        if self.active:
            color = COIN_COLORS[self.value]

            # Different coin values have different sizes
            if self.value == 1:
                radius = 14
            elif self.value == 3:
                radius = 10
            else:
                radius = 7

            pygame.draw.circle(screen, color, self.rect.center, radius)


# ===================== OBSTACLE =====================
# Road obstacles: oil, barrier, pothole
class Obstacle:
    def __init__(self, kind):
        self.kind = kind
        self.rect = pygame.Rect(0, 0, 45, 35)
        self.reset()

    def reset(self):
        # Spawn obstacle above the screen
        lane = random.choice(LANES)
        self.rect.x = lane
        self.rect.y = random.randint(-1200, -500)

    def move(self, speed):
        self.rect.y += speed

        # Respawn obstacle when it leaves the screen
        if self.rect.top > HEIGHT:
            self.reset()

    def draw(self, screen):
        # Oil spill: moves player sideways
        if self.kind == "oil":
            pygame.draw.ellipse(screen, OIL_COLOR, self.rect)

        # Barrier: causes crash
        elif self.kind == "barrier":
            pygame.draw.rect(screen, BARRIER_COLOR, self.rect, border_radius=5)
            pygame.draw.line(screen, WHITE, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(screen, WHITE, self.rect.topright, self.rect.bottomleft, 3)

        # Pothole: causes crash
        elif self.kind == "pothole":
            pygame.draw.ellipse(screen, BLACK, self.rect)


# ===================== POWER UP =====================
# Three power-ups: Nitro, Shield, Repair
class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 28, 28)
        self.active = False
        self.kind = None
        self.spawn_time = 0
        self.timer = random.randint(180, 360)

    def spawn(self, blocked_rects):
        # Choose random power-up type
        self.kind = random.choice(["nitro", "shield", "repair"])

        # Try to spawn without overlapping other objects
        for _ in range(50):
            lane = random.choice(LANES)
            self.rect.x = lane + 6
            self.rect.y = random.randint(-500, -80)

            if not any(self.rect.colliderect(r) for r in blocked_rects):
                break

        self.active = True
        self.spawn_time = pygame.time.get_ticks()

    def update(self, speed, blocked_rects):
        now = pygame.time.get_ticks()

        # Power-up appears after a timer
        if not self.active:
            self.timer -= 1

            if self.timer <= 0:
                self.spawn(blocked_rects)

            return

        self.rect.y += speed

        # Power-up disappears after 8 seconds or after leaving screen
        if self.rect.top > HEIGHT or now - self.spawn_time > 8000:
            self.active = False
            self.timer = random.randint(180, 360)

    def draw(self, screen):
        if not self.active:
            return

        # N = Nitro, S = Shield, R = Repair
        if self.kind == "nitro":
            color = NITRO_COLOR
            text = "N"
        elif self.kind == "shield":
            color = SHIELD_COLOR
            text = "S"
        else:
            color = REPAIR_COLOR
            text = "R"

        pygame.draw.circle(screen, color, self.rect.center, 15)

        label = font.render(text, True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)


# ===================== ROAD =====================
# Draws the road and lane lines
def draw_road(screen):
    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)

    # Lane lines
    pygame.draw.line(screen, WHITE, (160, 0), (160, HEIGHT), 1)
    pygame.draw.line(screen, WHITE, (240, 0), (240, HEIGHT), 1)


# ===================== GAME OVER SCREEN =====================
# Shows result and buttons after crash
def game_over_screen(screen, username, score, coins, level, distance):
    retry_btn = pygame.Rect(100, 390, 200, 45)
    menu_btn = pygame.Rect(100, 450, 200, 45)

    while True:
        screen.fill((150, 0, 0))

        title = big_font.render("GAME OVER", True, WHITE)
        screen.blit(title, (85, 80))

        screen.blit(font.render(f"Player: {username}", True, WHITE), (100, 160))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (100, 195))
        screen.blit(font.render(f"Coins: {coins}", True, WHITE), (100, 230))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (100, 265))
        screen.blit(font.render(f"Distance: {distance}", True, WHITE), (100, 300))

        pygame.draw.rect(screen, WHITE, retry_btn, border_radius=8)
        pygame.draw.rect(screen, WHITE, menu_btn, border_radius=8)

        retry_text = font.render("Retry", True, BLACK)
        menu_text = font.render("Main Menu", True, BLACK)

        screen.blit(retry_text, retry_text.get_rect(center=retry_btn.center))
        screen.blit(menu_text, menu_text.get_rect(center=menu_btn.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"


# ===================== GAME LOOP =====================
# Main gameplay function
def game_loop(screen, username):
    clock = pygame.time.Clock()

    while True:
        # Load settings from settings.json
        settings = load_settings()

        difficulty = settings["difficulty"]
        player_color = tuple(settings["car_color"])

        # Difficulty affects starting speed
        if difficulty == "easy":
            base_speed = 2.8
        elif difficulty == "hard":
            base_speed = 4.2
        else:
            base_speed = 3.4

        # Create game objects
        player = Player(player_color)
        enemies = [Enemy()]
        obstacles = []
        coin = Coin()
        powerup = PowerUp()

        # Game statistics
        score = 0
        coins = 0
        level = 1
        distance = 0

        # Active power-up state
        active_power = None
        power_end_time = 0

        running = True

        while running:
            clock.tick(FPS)
            now = pygame.time.get_ticks()

            # ===================== EVENTS =====================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ===================== LEVEL AND SPEED =====================
            # Level increases by distance
            level = distance // 500 + 1

            # Speed increases slowly with level
            speed = base_speed + (level - 1) * 0.25

            # Nitro temporarily increases speed
            if active_power == "nitro":
                speed += 3

                if now > power_end_time:
                    active_power = None

            # ===================== SPAWN OBSTACLES =====================
            # Only one obstacle can appear at the same time
            max_obstacles = 0

            if level >= 3:
                max_obstacles = 1

            visible_obstacles = [
                obs for obs in obstacles
                if -100 < obs.rect.y < HEIGHT
            ]

            if len(visible_obstacles) < max_obstacles and len(obstacles) < max_obstacles:
                if random.randint(1, 180) == 1:
                    kind = random.choice(["oil", "barrier", "pothole"])
                    new_obstacle = Obstacle(kind)

                    # Do not spawn too close to player
                    if abs(new_obstacle.rect.y - player.rect.y) > 300:
                        obstacles.append(new_obstacle)

            # ===================== SPAWN ENEMIES =====================
            # Usually only one traffic car appears at a time
            max_enemies = 1

            # On hard difficulty after level 5, maximum can be 2
            if difficulty == "hard" and level >= 5:
                max_enemies = 2

            visible_enemies = [
                enemy for enemy in enemies
                if -100 < enemy.rect.y < HEIGHT
            ]

            if len(visible_enemies) < max_enemies and len(enemies) < max_enemies:
                if random.randint(1, 220) == 1:
                    enemies.append(Enemy())

            # ===================== UPDATE OBJECTS =====================
            player.move()

            blocked_rects = [enemy.rect for enemy in enemies] + [obs.rect for obs in obstacles]

            for enemy in enemies:
                enemy.move(speed)

            for obs in obstacles:
                obs.move(speed)

            coin.update(speed, blocked_rects)
            powerup.update(speed, blocked_rects)

            # ===================== SCORE AND DISTANCE =====================
            distance += int(speed)
            score = coins * 10 + distance // 10

            # ===================== COIN COLLECTION =====================
            if coin.active and player.rect.colliderect(coin.rect):
                coins += coin.value

                coin.active = False
                coin.timer = random.randint(40, 120)

            # ===================== POWER-UP COLLECTION =====================
            if powerup.active and player.rect.colliderect(powerup.rect):
                # Only one timed power-up can be active at a time
                if active_power is None:
                    if powerup.kind == "nitro":
                        active_power = "nitro"
                        power_end_time = now + 5000

                    elif powerup.kind == "shield":
                        player.shield = True

                    elif powerup.kind == "repair":
                        # Repair removes one obstacle from the road
                        if obstacles:
                            obstacles.pop()

                powerup.active = False
                powerup.timer = random.randint(180, 360)

            # ===================== COLLISION DETECTION =====================
            crashed = False
            hit_enemy = None
            hit_obstacle = None

            # Collision with traffic cars
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    crashed = True
                    hit_enemy = enemy

            # Collision with road obstacles
            for obs in obstacles:
                if player.rect.colliderect(obs.rect):
                    if obs.kind == "oil":
                        # Oil does not end the game, it pushes the car sideways
                        player.rect.x += random.choice([-20, 20])
                        player.rect.x = max(
                            ROAD_LEFT,
                            min(player.rect.x, ROAD_RIGHT - player.rect.width)
                        )
                    else:
                        crashed = True
                        hit_obstacle = obs

            # ===================== SHIELD LOGIC =====================
            # Shield protects from one collision
            if crashed:
                if player.shield:
                    player.shield = False

                    # Remove or reset the object that caused collision
                    if hit_enemy:
                        hit_enemy.reset()

                    if hit_obstacle and hit_obstacle in obstacles:
                        obstacles.remove(hit_obstacle)

                else:
                    # Save result to leaderboard.json
                    save_score(username, score, coins, level, distance)

                    result = game_over_screen(screen, username, score, coins, level, distance)

                    if result == "retry":
                        running = False

                    elif result == "menu":
                        return

            # ===================== DRAW EVERYTHING =====================
            draw_road(screen)

            for obs in obstacles:
                obs.draw(screen)

            coin.draw(screen)
            powerup.draw(screen)

            for enemy in enemies:
                enemy.draw(screen)

            player.draw(screen)

            # ===================== GAME UI =====================
            screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
            screen.blit(font.render(f"Coins: {coins}", True, BLACK), (10, 35))
            screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 60))
            screen.blit(font.render(f"Distance: {distance}", True, BLACK), (10, 85))

            # Show nitro timer
            if active_power == "nitro":
                left = max(0, (power_end_time - now) // 1000)
                screen.blit(font.render(f"Nitro: {left}s", True, BLACK), (250, 35))

            # Show shield status
            if player.shield:
                screen.blit(font.render("Shield: ON", True, BLACK), (250, 60))

            pygame.display.update()