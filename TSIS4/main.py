import pygame
import sys
from db import create_tables
from game import main_menu, leaderboard_screen, settings_screen, game_loop

pygame.init()

# ===================== SCREEN =====================
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")

# ===================== DATABASE INIT =====================
create_tables()

# ===================== MAIN LOOP =====================
while True:
    action, username = main_menu(screen)

    if action == "play":
        game_loop(screen, username)

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        settings_screen(screen)

    elif action == "quit":
        pygame.quit()
        sys.exit()