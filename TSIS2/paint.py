import pygame
from tools import get_canvas_pos, flood_fill, save_canvas, draw_shape

pygame.init()

WIDTH, HEIGHT = 1200, 750
TOOLBAR_HEIGHT = 170

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")
clock = pygame.time.Clock()

tool = "brush"
color = "blue"
size = 5

drawing = False
start_pos = None
current_mouse = None
last_pos = None

text_mode = False
text_pos = None
text_input = ""

COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

ERASER_COLOR = (255, 255, 255)

font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)
text_font = pygame.font.SysFont(None, 32)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

color_rects = {
    "black": pygame.Rect(20, 55, 42, 42),
    "red": pygame.Rect(75, 55, 42, 42),
    "green": pygame.Rect(130, 55, 42, 42),
    "blue": pygame.Rect(185, 55, 42, 42),
}

tool_rects = {
    "brush": pygame.Rect(300, 45, 95, 38),
    "line": pygame.Rect(410, 45, 95, 38),
    "rect": pygame.Rect(520, 45, 95, 38),
    "circle": pygame.Rect(630, 45, 95, 38),
    "eraser": pygame.Rect(740, 45, 95, 38),
    "fill": pygame.Rect(850, 45, 95, 38),
    "text": pygame.Rect(960, 45, 95, 38),
}

shape_rects = {
    "square": pygame.Rect(300, 105, 95, 38),
    "right_triangle": pygame.Rect(410, 105, 150, 38),
    "equilateral_triangle": pygame.Rect(575, 105, 190, 38),
    "rhombus": pygame.Rect(780, 105, 120, 38),
}


def draw_button(rect, text, active=False):
    bg = (185, 255, 185) if active else (248, 248, 248)
    pygame.draw.rect(screen, bg, rect, border_radius=10)
    pygame.draw.rect(screen, (45, 45, 45), rect, 2, border_radius=10)

    label = small_font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


running = True

while running:
    clock.tick(60)
    preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            elif event.key == pygame.K_1:
                size = 2
            elif event.key == pygame.K_2:
                size = 5
            elif event.key == pygame.K_3:
                size = 10

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    rendered_text = text_font.render(text_input, True, COLORS[color])
                    canvas.blit(rendered_text, text_pos)
                    text_mode = False
                    text_input = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < TOOLBAR_HEIGHT:
                for name, rect in color_rects.items():
                    if rect.collidepoint(mx, my):
                        color = name

                for name, rect in tool_rects.items():
                    if rect.collidepoint(mx, my):
                        tool = name

                for name, rect in shape_rects.items():
                    if rect.collidepoint(mx, my):
                        tool = name

            else:
                pos = get_canvas_pos(event.pos, TOOLBAR_HEIGHT)

                if tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], COLORS[color])

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    text_input = ""

                else:
                    drawing = True
                    start_pos = pos
                    current_mouse = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                current_mouse = get_canvas_pos(event.pos, TOOLBAR_HEIGHT)

                if tool == "brush":
                    pygame.draw.line(canvas, COLORS[color], last_pos, current_mouse, size)
                    last_pos = current_mouse

                elif tool == "eraser":
                    pygame.draw.line(canvas, ERASER_COLOR, last_pos, current_mouse, size)
                    last_pos = current_mouse

        if event.type == pygame.MOUSEBUTTONUP:
            if not drawing or start_pos is None:
                continue

            end_pos = get_canvas_pos(event.pos, TOOLBAR_HEIGHT)
            draw_color = ERASER_COLOR if tool == "eraser" else COLORS[color]

            draw_shape(canvas, tool, start_pos, end_pos, draw_color, size)

            drawing = False
            start_pos = None
            current_mouse = None
            last_pos = None

    if drawing and start_pos and current_mouse:
        draw_color = ERASER_COLOR if tool == "eraser" else COLORS[color]

        if tool in ["line", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
            draw_shape(preview, tool, start_pos, current_mouse, draw_color, size)

    screen.fill((235, 235, 235))

    pygame.draw.rect(screen, (205, 205, 205), (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, (90, 90, 90), (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 3)

    screen.blit(font.render("Colors", True, (0, 0, 0)), (20, 25))
    for name, rect in color_rects.items():
        pygame.draw.rect(screen, COLORS[name], rect, border_radius=8)
        border = 4 if color == name else 2
        pygame.draw.rect(screen, (0, 0, 0), rect, border, border_radius=8)

    screen.blit(font.render("Tools", True, (0, 0, 0)), (300, 18))
    for name, rect in tool_rects.items():
        draw_button(rect, name, tool == name)

    screen.blit(font.render("Shapes", True, (0, 0, 0)), (300, 82))
    for name, rect in shape_rects.items():
        draw_button(rect, name, tool == name)

    info_rect = pygame.Rect(20, 145, WIDTH - 40, 20)
    pygame.draw.rect(screen, (250, 250, 250), info_rect, border_radius=8)

    info = f"Tool: {tool}    Color: {color}    Size: {size}px       1=small    2=medium    3=large       Ctrl+S=save"
    screen.blit(small_font.render(info, True, (0, 0, 0)), (35, 148))

    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_mode and text_pos:
        temp_text = text_font.render(text_input + "|", True, COLORS[color])
        screen.blit(temp_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()

pygame.quit()