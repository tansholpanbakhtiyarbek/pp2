import pygame
import random
import sys

pygame.init()

# ===================== SCREEN SETTINGS =====================
WIDTH, HEIGHT = 400, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Lab 10")
clock = pygame.time.Clock()

# ===================== COLORS =====================
GREEN = (0, 180, 0)
GRAY = (110, 110, 110)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)

PLAYER_COLOR = (40, 120, 255)
ENEMY_COLOR = (220, 60, 60)

# ===================== ROAD =====================
ROAD_LEFT = 80
ROAD_RIGHT = 320

# ===================== GAME VARIABLES =====================
base_speed = 5
speed = base_speed

score = 0
coins = 0
level = 1

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)


# ===================== DRAW CAR FUNCTION =====================
# Draws a simple car using rectangles and circles
def draw_car(surface, rect, color):
    pygame.draw.rect(surface, color, rect, border_radius=8)

    # windows
    pygame.draw.rect(surface, BLACK,
                     (rect.x + 5, rect.y + 8, rect.width - 10, 15),
                     border_radius=4)

    # wheels
    pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.y + 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + rect.width - 8, rect.y + 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.y + rect.height - 10), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + rect.width - 8, rect.y + rect.height - 10), 5)


# ===================== PLAYER CLASS =====================
# Player controlled by keyboard (left/right movement)
class Player:
    def __init__(self):
        self.rect = pygame.Rect(180, 500, 40, 70)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += 6

    def draw(self):
        draw_car(screen, self.rect, PLAYER_COLOR)


# ===================== ENEMY CLASS =====================
# Enemy car that moves downward and increases score when passed
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 40, 70)
        self.reset()

    def reset(self):
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 50)
        self.rect.y = random.randint(-600, -50)

    def move(self):
        global score

        self.rect.y += speed

        if self.rect.top > HEIGHT:
            score += 1
            self.reset()

    def draw(self):
        draw_car(screen, self.rect, ENEMY_COLOR)


# ===================== COIN CLASS =====================
# Coin system: randomly spawns coins and tracks collection
class Coin:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.active = False
        self.timer = random.randint(40, 120)

    def spawn(self):
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 30)
        self.rect.y = random.randint(-300, -50)
        self.active = True

    def update(self):
        global coins

        if not self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.spawn()
            return

        self.rect.y += speed

        if self.rect.top > HEIGHT:
            self.active = False
            self.timer = random.randint(40, 120)

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, YELLOW, self.rect.center, 10)


# ===================== ROAD DRAW =====================
def draw_road():
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)


# ===================== GAME OVER SCREEN =====================
def game_over():
    while True:
        screen.fill((180, 0, 0))

        text1 = big_font.render("GAME OVER", True, WHITE)
        text2 = font.render("Press R to Restart", True, WHITE)
        text3 = font.render("Press Q to Quit", True, WHITE)

        screen.blit(text1, (70, 200))
        screen.blit(text2, (110, 300))
        screen.blit(text3, (120, 340))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return


# ===================== RESET GAME =====================
def reset_game():
    global speed, score, coins, level, player, enemy

    speed = base_speed
    score = 0
    coins = 0
    level = 1

    player = Player()
    enemy = Enemy()
    coin.active = False
    coin.timer = random.randint(40, 120)


# ===================== OBJECTS =====================
player = Player()
enemy = Enemy()
coin = Coin()

# ===================== MAIN LOOP =====================
while True:

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -------- LEVEL SYSTEM --------
    # Level increases every 5 points
    level = score // 5 + 1

    # Smooth speed increase
    speed = base_speed + (level - 1) * 0.6

    # -------- UPDATE --------
    player.move()
    enemy.move()
    coin.update()

    # Coin collection
    if coin.active and player.rect.colliderect(coin.rect):
        coins += 1
        coin.active = False
        coin.timer = random.randint(40, 120)

    # Collision with enemy
    if player.rect.colliderect(enemy.rect):
        game_over()
        reset_game()

    # -------- DRAW --------
    draw_road()

    player.draw()
    enemy.draw()
    coin.draw()

    # ===================== UI =====================
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 35))

    # Coins in TOP RIGHT (required)
    coin_text = font.render(f"Coins: {coins}", True, BLACK)
    coin_rect = coin_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(coin_text, coin_rect)

    pygame.display.update()
    clock.tick(FPS)