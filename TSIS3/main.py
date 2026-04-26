import pygame
import sys
from ui import main_menu, leaderboard_screen, settings_screen
from racer import game_loop

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

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