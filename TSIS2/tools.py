import pygame
import math
from datetime import datetime
from collections import deque


def get_canvas_pos(pos, toolbar_height):
    return pos[0], pos[1] - toolbar_height


def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def save_canvas(canvas):
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_shape(surface, tool, start_pos, end_pos, color, size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    if tool == "line":
        pygame.draw.line(surface, color, start_pos, end_pos, size)

    elif tool == "rect":
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)),
            size
        )

    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, pygame.Rect(x1, y1, side, side), size)

    elif tool == "circle":
        radius = int(math.dist(start_pos, end_pos))
        pygame.draw.circle(surface, color, start_pos, radius, size)

    elif tool == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "equilateral_triangle":
        side = abs(x2 - x1)
        height = int(math.sqrt(3) / 2 * side)

        points = [
            (x1, y2),
            (x1 + side, y2),
            (x1 + side // 2, y2 - height)
        ]

        pygame.draw.polygon(surface, color, points, size)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        dx = abs(x2 - x1) // 2
        dy = abs(y2 - y1) // 2

        points = [
            (cx, cy - dy),
            (cx + dx, cy),
            (cx, cy + dy),
            (cx - dx, cy)
        ]

        pygame.draw.polygon(surface, color, points, size)