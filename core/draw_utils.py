"""
Utilidades de dibujo reutilizables.
"""

import pygame
import math
from core.constants import C_DIM, C_CODE_BG


def draw_panel(surf: pygame.Surface, rect: pygame.Rect,
               bg=(10, 21, 32), border=(0, 255, 255), alpha=60, border_w=1):
    """Panel semitransparente con borde cyan."""
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((*bg, alpha))
    surf.blit(s, rect.topleft)
    pygame.draw.rect(surf, border, rect, border_w)


def draw_glow_circle(surf: pygame.Surface, center, radius: int,
                     color, intensity: float = 1.0):
    """Círculo con resplandor radial."""
    glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    r, g, b = color[:3]
    for i in range(radius * 2, 0, -4):
        a = int(60 * intensity * (i / (radius * 2)))
        pygame.draw.circle(glow, (r, g, b, a),
                           (radius * 2, radius * 2), i)
    surf.blit(glow, (center[0] - radius * 2, center[1] - radius * 2))
    pygame.draw.circle(surf, color, center, radius, 2)


def draw_arrow_line(
        surf: pygame.Surface, start, end,
        color, width=2, alpha=255):
    """Línea punteada con flecha en el medio."""
    line_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    ax, ay = start
    bx, by = end

    # Línea punteada
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    dash_len, gap_len = 8, 5
    pos = 0
    drawing = True
    while pos < length:
        seg = min(dash_len if drawing else gap_len, length - pos)
        sx, sy = ax + ux * pos, ay + uy * pos
        ex2, ey2 = ax + ux * (pos + seg), ay + uy * (pos + seg)
        if drawing:
            pygame.draw.line(line_surf, (*color[:3], alpha),
                             (int(sx), int(sy)), (int(ex2), int(ey2)), width)
        pos += seg
        drawing = not drawing

    # Flecha en el medio
    mx, my = (ax + bx) / 2, (ay + by) / 2
    angle = math.atan2(dy, dx)
    arrow_size = 10
    p1 = (mx, my)
    p2 = (mx - arrow_size * math.cos(angle - 0.4),
          my - arrow_size * math.sin(angle - 0.4))
    p3 = (mx - arrow_size * math.cos(angle + 0.4),
          my - arrow_size * math.sin(angle + 0.4))
    pygame.draw.polygon(line_surf, (*color[:3], alpha),
                        [(int(x), int(y)) for x, y in [p1, p2, p3]])
    surf.blit(line_surf, (0, 0))


def draw_progress_bar(surf: pygame.Surface, rect: pygame.Rect,
                      value: float, color=(0, 255, 136), bg=(26, 48, 64)):
    """Barra de progreso estilo cyberpunk."""
    pygame.draw.rect(surf, bg, rect, border_radius=2)
    if value > 0:
        fill = rect.copy()
        fill.width = int(rect.width * min(1.0, value))
        pygame.draw.rect(surf, color, fill, border_radius=2)
    pygame.draw.rect(surf, C_DIM, rect, 1, border_radius=2)


def render_text_with_outline(surf: pygame.Surface, font: pygame.font.Font,
                             text: str, color: tuple, pos: tuple,
                             outline_color=(0, 0, 0)):
    """Dibuja texto con contorno oscuro.

    Mejora legibilidad en fondos oscuros."""
    x, y = pos
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ts = font.render(text, True, outline_color)
        surf.blit(ts, (x + dx, y + dy))
    ts = font.render(text, True, color)
    surf.blit(ts, (x, y))


def render_text_lines(surf: pygame.Surface, lines: list,
                      font: pygame.font.Font, color, x: int, y: int,
                      line_height: int = None) -> int:
    """Renderiza una lista de strings y devuelve la Y final."""
    lh = line_height or font.get_linesize() + 2
    for line in lines:
        if line:
            text_surf = font.render(line, True, color)
            surf.blit(text_surf, (x, y))
        y += lh
    return y
