import pygame
from persistence import load_leaderboard, load_settings, save_settings

pygame.init()

WIDTH, HEIGHT = 400, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
DARK_GRAY = (80, 80, 80)
BLUE = (50, 120, 255)

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 34)


def draw_button(screen, rect, text):
    pygame.draw.rect(screen, GRAY, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def main_menu(screen):
    username = ""

    play_btn = pygame.Rect(100, 230, 200, 45)
    leaderboard_btn = pygame.Rect(100, 285, 200, 45)
    settings_btn = pygame.Rect(100, 340, 200, 45)
    quit_btn = pygame.Rect(100, 395, 200, 45)

    while True:
        screen.fill((220, 220, 220))

        title = big_font.render("RACER GAME", True, BLACK)
        screen.blit(title, (80, 60))

        name_label = font.render("Username:", True, BLACK)
        screen.blit(name_label, (100, 130))

        pygame.draw.rect(screen, WHITE, (100, 160, 200, 40), border_radius=8)
        pygame.draw.rect(screen, BLACK, (100, 160, 200, 40), 2, border_radius=8)

        name_text = font.render(username + "|", True, BLACK)
        screen.blit(name_text, (110, 168))

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
                if play_btn.collidepoint(event.pos):
                    if username.strip() != "":
                        return "play", username

                if leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard", username

                if settings_btn.collidepoint(event.pos):
                    return "settings", username

                if quit_btn.collidepoint(event.pos):
                    return "quit", username


def leaderboard_screen(screen):
    back_btn = pygame.Rect(120, 530, 160, 45)

    while True:
        screen.fill((230, 230, 230))

        title = big_font.render("TOP 10", True, BLACK)
        screen.blit(title, (135, 30))

        data = load_leaderboard()

        header = font.render("Rank  Name     Score  Dist", True, BLACK)
        screen.blit(header, (30, 100))

        y = 140
        for i, item in enumerate(data):
            row = font.render(
                f"{i + 1}. {item['name'][:7]:7} {item['score']:5} {item['distance']:5}",
                True,
                BLACK
            )
            screen.blit(row, (30, y))
            y += 35

        draw_button(screen, back_btn, "Back")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen(screen):
    settings = load_settings()

    sound_btn = pygame.Rect(90, 180, 220, 45)
    difficulty_btn = pygame.Rect(90, 245, 220, 45)
    color_btn = pygame.Rect(90, 310, 220, 45)
    save_btn = pygame.Rect(90, 430, 220, 45)

    colors = [
        [40, 120, 255],
        [255, 60, 60],
        [60, 200, 80],
        [255, 180, 40]
    ]

    difficulties = ["easy", "medium", "hard"]

    while True:
        screen.fill((230, 230, 230))

        title = big_font.render("SETTINGS", True, BLACK)
        screen.blit(title, (95, 60))

        draw_button(screen, sound_btn, f"Sound: {settings['sound']}")
        draw_button(screen, difficulty_btn, f"Difficulty: {settings['difficulty']}")
        draw_button(screen, color_btn, "Change Car Color")
        draw_button(screen, save_btn, "Save & Back")

        pygame.draw.rect(screen, settings["car_color"], (170, 370, 60, 40), border_radius=8)
        pygame.draw.rect(screen, BLACK, (170, 370, 60, 40), 2, border_radius=8)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif difficulty_btn.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

                elif color_btn.collidepoint(event.pos):
                    current = settings["car_color"]
                    index = colors.index(current) if current in colors else 0
                    settings["car_color"] = colors[(index + 1) % len(colors)]

                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return