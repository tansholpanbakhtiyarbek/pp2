import pygame
import math

pygame.init()

# ===================== SCREEN =====================
# Create main window for drawing
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# ===================== STATE =====================
# Current tool and drawing settings
tool = "brush"
color = "blue"
size = 5

start_pos = None
current_mouse = None
drawing = False
points = []

# ===================== COLORS =====================
# Available drawing colors
COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

# Color used for eraser (white background)
ERASER_COLOR = (255, 255, 255)

# ===================== UI ELEMENTS =====================
# Color selection buttons
color_rects = {
    "black": pygame.Rect(10, 10, 40, 40),
    "red": pygame.Rect(60, 10, 40, 40),
    "green": pygame.Rect(110, 10, 40, 40),
    "blue": pygame.Rect(160, 10, 40, 40),
}

# Tools (basic shapes)
tool_rects = {
    "brush": pygame.Rect(250, 10, 80, 40),
    "rect": pygame.Rect(340, 10, 80, 40),
    "circle": pygame.Rect(430, 10, 80, 40),
    "eraser": pygame.Rect(520, 10, 80, 40),
}

# Advanced shapes (required tasks)
shape_rects = {
    "square": pygame.Rect(250, 60, 80, 40),
    "right_triangle": pygame.Rect(340, 60, 140, 40),
    "equilateral_triangle": pygame.Rect(490, 60, 180, 40),
    "rhombus": pygame.Rect(680, 60, 100, 40),
}

# Drawing canvas (separate surface to preserve drawings)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont(None, 20)

# ===================== MAIN LOOP =====================
running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===================== SIZE CONTROL =====================
        # Increase / decrease brush size
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                size = min(50, size + 1)

            if event.key == pygame.K_MINUS:
                size = max(1, size - 1)

        # ===================== MOUSE CLICK =====================
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # UI area (top panel)
            if my < 100:

                # Select color
                for name, rect in color_rects.items():
                    if rect.collidepoint(mx, my):
                        color = name

                # Select tool
                for name, rect in tool_rects.items():
                    if rect.collidepoint(mx, my):
                        tool = name

                # Select shape tool
                for name, rect in shape_rects.items():
                    if rect.collidepoint(mx, my):
                        tool = name

            else:
                drawing = True
                start_pos = (mx, my - 100)
                current_mouse = start_pos

                if tool == "brush":
                    points = [start_pos]

        # ===================== DRAWING (MOTION) =====================
        if event.type == pygame.MOUSEMOTION:
            current_mouse = event.pos

            if drawing:
                mx, my = event.pos
                pos = (mx, my - 100)

                # Freehand drawing
                if tool == "brush":
                    points.append(pos)

                # Eraser (draws white circles)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, ERASER_COLOR, pos, size)

        # ===================== FINAL SHAPES =====================
        if event.type == pygame.MOUSEBUTTONUP:

            if not start_pos:
                continue

            end = event.pos
            end = (end[0], end[1] - 100)

            x1, y1 = start_pos
            x2, y2 = end

            # Choose drawing color
            c = ERASER_COLOR if tool == "eraser" else COLORS[color]

            # -------- RECTANGLE --------
            if tool == "rect":
                pygame.draw.rect(canvas, c,
                                 pygame.Rect(min(x1, x2), min(y1, y2),
                                             abs(x1 - x2), abs(y1 - y2)), size)

            # -------- SQUARE --------
            elif tool == "square":
                side = max(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(canvas, c, pygame.Rect(x1, y1, side, side), size)

            # -------- CIRCLE --------
            elif tool == "circle":
                r = int(math.dist(start_pos, end))
                pygame.draw.circle(canvas, c, start_pos, r, size)

            # -------- RIGHT TRIANGLE --------
            elif tool == "right_triangle":
                pts = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(canvas, c, pts, size)

            # -------- EQUILATERAL TRIANGLE (REQUIRED TASK) --------
            # All sides are equal
            elif tool == "equilateral_triangle":
                side = abs(x2 - x1)
                height = int(math.sqrt(3) / 2 * side)

                pts = [
                    (x1, y2),
                    (x1 + side, y2),
                    (x1 + side // 2, y2 - height)
                ]
                pygame.draw.polygon(canvas, c, pts, size)

            # -------- RHOMBUS --------
            # Built using center-based geometry
            elif tool == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2

                pts = [
                    (cx, cy - dy),
                    (cx + dx, cy),
                    (cx, cy + dy),
                    (cx - dx, cy)
                ]
                pygame.draw.polygon(canvas, c, pts, size)

            drawing = False
            start_pos = None
            points = []

    # ===================== DRAW UI =====================
    screen.fill((220, 220, 220))
    pygame.draw.rect(screen, (180, 180, 180), (0, 0, WIDTH, 100))

    # Color buttons
    for name, rect in color_rects.items():
        pygame.draw.rect(screen, COLORS[name], rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    # Tools
    for name, rect in tool_rects.items():
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        screen.blit(font.render(name, True, (0, 0, 0)), (rect.x + 2, rect.y + 10))

    # Shapes
    for name, rect in shape_rects.items():
        pygame.draw.rect(screen, (240, 240, 240), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        screen.blit(font.render(name, True, (0, 0, 0)), (rect.x + 2, rect.y + 10))

    # Draw canvas
    screen.blit(canvas, (0, 100))

    # Brush preview
    if tool == "brush" and len(points) > 1:
        for i in range(len(points) - 1):
            pygame.draw.line(canvas, COLORS[color], points[i], points[i + 1], size)

    pygame.display.flip()

pygame.quit()