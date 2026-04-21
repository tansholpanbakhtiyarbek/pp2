import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()

    # ---------------- STATE ----------------
    tool = "brush"
    color = "blue"

    size = 8
    points = []

    start_pos = None
    current_mouse = None
    drawing = False

    # ---------------- COLORS ----------------
    COLORS = {
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    # ---------------- UI ----------------
    color_rects = {
        "black": pygame.Rect(10, 10, 40, 40),
        "red": pygame.Rect(60, 10, 40, 40),
        "green": pygame.Rect(110, 10, 40, 40),
        "blue": pygame.Rect(160, 10, 40, 40),
    }

    tool_rects = {
        "brush": pygame.Rect(250, 10, 80, 40),
        "rect": pygame.Rect(340, 10, 80, 40),
        "circle": pygame.Rect(430, 10, 80, 40),
        "eraser": pygame.Rect(520, 10, 80, 40),
    }

    plus_btn = pygame.Rect(650, 10, 40, 40)
    minus_btn = pygame.Rect(700, 10, 40, 40)

    canvas = pygame.Surface((900, 600))
    canvas.fill((255, 255, 255))

    font = pygame.font.SysFont(None, 24)

    # ---------------- LOOP ----------------
    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            # -------- CLICK --------
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if my < 70:
                    # colors
                    for name, rect in color_rects.items():
                        if rect.collidepoint(mx, my):
                            color = name

                    # tools
                    for name, rect in tool_rects.items():
                        if rect.collidepoint(mx, my):
                            tool = name

                    # size controls
                    if plus_btn.collidepoint(mx, my):
                        size = min(50, size + 1)

                    if minus_btn.collidepoint(mx, my):
                        size = max(1, size - 1)

                else:
                    drawing = True
                    start_pos = (mx, my - 70)
                    current_mouse = start_pos

                    if tool == "brush":
                        points.append(start_pos)

            # -------- MOVE --------
            if event.type == pygame.MOUSEMOTION:
                current_mouse = event.pos

                if drawing:
                    mx, my = event.pos
                    pos = (mx, my - 70)

                    if tool == "brush":
                        points.append(pos)

                    elif tool == "eraser":
                        pygame.draw.circle(canvas, (255, 255, 255), pos, size)

            # -------- RELEASE --------
            if event.type == pygame.MOUSEBUTTONUP:

                if tool == "rect" and start_pos:
                    end = event.pos
                    end = (end[0], end[1] - 70)

                    x1, y1 = start_pos
                    x2, y2 = end

                    rect = pygame.Rect(
                        min(x1, x2),
                        min(y1, y2),
                        abs(x1 - x2),
                        abs(y1 - y2)
                    )

                    pygame.draw.rect(canvas, COLORS[color], rect, max(1, size))

                elif tool == "circle" and start_pos:
                    end = event.pos
                    end = (end[0], end[1] - 70)

                    r = int(math.dist(start_pos, end))
                    pygame.draw.circle(canvas, COLORS[color], start_pos, r, max(1, size))

                drawing = False
                start_pos = None
                points = []

        # ---------------- DRAW ----------------
        screen.fill((220, 220, 220))

        pygame.draw.rect(screen, (180, 180, 180), (0, 0, 900, 70))

        # colors
        for name, rect in color_rects.items():
            pygame.draw.rect(screen, COLORS[name], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # tools
        for name, rect in tool_rects.items():
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            txt = font.render(name, True, (0, 0, 0))
            screen.blit(txt, (rect.x + 10, rect.y + 10))

        # size buttons
        pygame.draw.rect(screen, (200, 200, 200), plus_btn)
        pygame.draw.rect(screen, (200, 200, 200), minus_btn)

        screen.blit(font.render("+", True, (0, 0, 0)), (plus_btn.x + 12, plus_btn.y + 8))
        screen.blit(font.render("-", True, (0, 0, 0)), (minus_btn.x + 12, minus_btn.y + 8))

        screen.blit(font.render(f"Size: {size}", True, (0, 0, 0)), (750, 20))

        # canvas
        screen.blit(canvas, (0, 70))

        # brush render
        if tool == "brush" and len(points) > 1:
            for i in range(len(points) - 1):
                pygame.draw.line(canvas, COLORS[color], points[i], points[i + 1], size)

        # preview shapes
        if drawing and start_pos and current_mouse and tool in ("rect", "circle"):

            x1, y1 = start_pos
            x2, y2 = current_mouse

            y1 -= 70
            y2 -= 70

            if tool == "rect":
                rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x1 - x2),
                    abs(y1 - y2)
                )
                pygame.draw.rect(screen, COLORS[color], rect, 2)

            elif tool == "circle":
                r = int(math.dist((x1, y1), (x2, y2)))
                pygame.draw.circle(screen, COLORS[color], (x1, y1), r, 2)

        pygame.display.flip()

main()