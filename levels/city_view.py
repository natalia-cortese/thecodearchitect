"""
Vista de la ciudad digital — canvas animado de la izquierda.
Muestra edificios, cables (enredados o limpios) y nodos de clases.
"""

import pygame
import math
import random
from core.constants import *
from core.fonts import get_font
from core.draw_utils import draw_glow_circle, draw_arrow_line, render_text_with_outline
from core.state import GameState


class Building:
    def __init__(self, x, y, w, h):
        self.rect   = pygame.Rect(x, y, w, h)
        shade       = random.randint(8, 18)
        self.color  = (shade, shade + 4, shade + 8)
        self.windows: list[Window] = []
        self._gen_windows()

    def _gen_windows(self):
        cols = max(1, self.rect.width  // 13)
        rows = max(1, self.rect.height // 17)
        for r in range(rows):
            for c in range(cols):
                wx = self.rect.x + 4 + c * 13
                wy = self.rect.y + 6 + r * 17
                self.windows.append(Window(wx, wy, random.random() > 0.4))

    def draw(self, surf: pygame.Surface, broken: bool, frame: int):
        pygame.draw.rect(surf, self.color, self.rect)
        for win in self.windows:
            win.draw(surf, broken, frame)
        # Borde superior con glow
        top_color = C_DANGER if broken else C_CYAN
        glow_surf = pygame.Surface((self.rect.width, 4), pygame.SRCALPHA)
        glow_surf.fill((*top_color, 40))
        surf.blit(glow_surf, (self.rect.x, self.rect.y - 2))


class Window:
    def __init__(self, x, y, lit: bool):
        self.rect    = pygame.Rect(x, y, 7, 9)
        self.lit     = lit
        self.flicker = random.random() > 0.82
        self.phase   = random.uniform(0, math.pi * 2)

    def draw(self, surf: pygame.Surface, broken: bool, frame: int):
        lit = self.lit
        if self.flicker and broken:
            lit = math.sin(frame * 0.12 + self.phase) > 0
        if lit:
            color = (255, 50, 50) if broken else (255, 220, 90)
        else:
            color = (12, 20, 28)
        pygame.draw.rect(surf, color, self.rect)


class Wire:
    """Cable bezier animado para mostrar acoplamiento caótico."""
    def __init__(self, w, h):
        self.p0 = (random.randint(0, w), random.randint(0, h))
        self.p3 = (random.randint(0, w), random.randint(0, h))
        self.c1 = (random.randint(0, w), random.randint(0, h))
        self.c2 = (random.randint(0, w), random.randint(0, h))
        hue     = random.randint(180, 240)
        self.color  = pygame.Color(0)
        self.color.hsva = (hue, 100, 80, 100)
        self.alpha  = random.uniform(0.12, 0.35)
        self.phase  = random.uniform(0, math.pi * 2)
        self.speed  = random.uniform(0.015, 0.04)
        self._pts   = []
        self._regen_points()

    def _regen_points(self, jitter=0.0):
        pts = []
        for t in [i / 20 for i in range(21)]:
            mt = 1 - t
            x = (mt**3 * self.p0[0]
                 + 3 * mt**2 * t * self.c1[0]
                 + 3 * mt * t**2 * self.c2[0]
                 + t**3 * self.p3[0])
            y = (mt**3 * self.p0[1]
                 + 3 * mt**2 * t * self.c1[1]
                 + 3 * mt * t**2 * self.c2[1]
                 + t**3 * self.p3[1])
            pts.append((int(x + jitter * math.sin(t * math.pi)), int(y)))
        self._pts = pts

    def update(self):
        self.phase += self.speed
        jitter = math.sin(self.phase) * 10
        self._regen_points(jitter)

    def draw(self, surf: pygame.Surface, fade: float = 1.0):
        if len(self._pts) < 2 or fade <= 0:
            return
        a = int(self.alpha * fade * 255)
        r, g, b = self.color.r, self.color.g, self.color.b
        wire_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        pygame.draw.lines(wire_surf, (r, g, b, a), False, self._pts, 2)
        surf.blit(wire_surf, (0, 0))


class ClassNode:
    """Nodo visual que representa una clase Python."""
    def __init__(self, label: str, color, radius: int = 28):
        self.label   = label
        self.color   = color
        self.radius  = radius
        self.visible = False
        self.x = 0
        self.y = 0
        self._appear = 0.0   # animación de aparición 0→1

    def update(self, dt: float):
        if self.visible and self._appear < 1.0:
            self._appear = min(1.0, self._appear + dt * 2)

    def draw(self, surf: pygame.Surface, frame: int):
        if not self.visible or self._appear <= 0:
            return
        alpha = int(self._appear * 255)
        pulse = math.sin(frame * 0.05) * 5

        draw_glow_circle(surf, (self.x, self.y),
                         int(self.radius + pulse), self.color,
                         intensity=self._appear * 0.8)

        # Fondo oscuro del círculo
        pygame.draw.circle(surf, C_CODE_BG, (self.x, self.y), self.radius)
        pygame.draw.circle(surf, self.color,  (self.x, self.y), self.radius, 2)

        # Label: texto blanco sobre el círculo oscuro para que el nombre se lea bien
        font = get_font(13, "mono", bold=True)
        text_color = (255, 255, 255)
        words = self.label.split()
        for i, word in enumerate(words):
            dy = -6 + i * 16
            tw = font.size(word)[0]
            th = font.get_height()
            cx = self.x
            cy = self.y + dy
            render_text_with_outline(surf, font, word, text_color,
                                     (cx - tw // 2, cy - th // 2),
                                     outline_color=(2, 6, 10))


class CityView:
    def __init__(self, width: int, height: int):
        self.width  = width
        self.height = height
        self.surf   = pygame.Surface((width, height))
        self.frame  = 0

        self._build_scene()

    def _build_scene(self):
        random.seed(42)   # escena reproducible
        w, h = self.width, self.height

        # Edificios
        self.buildings: list[Building] = []
        num_b = 14
        for i in range(num_b):
            bw = random.randint(35, 75)
            bh = random.randint(80, 220)
            bx = int(w / num_b * i) + random.randint(0, 15)
            by = h - bh - 30
            self.buildings.append(Building(bx, by, bw, bh))

        # Cables caóticos
        self.wires = [Wire(w, h) for _ in range(20)]

        # Nodos de clases
        self.node_video = ClassNode("Video",           C_DANGER,  32)
        self.node_stats = ClassNode("VideoStats",      C_SUCCESS, 24)
        self.node_repo  = ClassNode("VideoRepository", C_CYAN,    24)
        self.node_video.visible = True
        self.node_video._appear = 1.0

        self._update_node_positions()

    def _update_node_positions(self):
        w, h = self.width, self.height
        self.node_video.x = w // 2;  self.node_video.y = int(h * 0.35)
        self.node_stats.x = int(w * 0.28); self.node_stats.y = int(h * 0.58)
        self.node_repo.x  = int(w * 0.72); self.node_repo.y  = int(h * 0.58)

    def draw(self) -> pygame.Surface:
        surf = self.surf
        surf.fill(C_BG)

        # Gradiente de cielo
        sky = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y in range(self.height):
            ratio = y / self.height
            a = int(30 * (1 - ratio))
            pygame.draw.line(sky, (0, 40, 60, a), (0, y), (self.width, y))
        surf.blit(sky, (0, 0))

        # Edificios
        for b in self.buildings:
            b.draw(surf, self._state_broken, self.frame)

        # Suelo
        ground = pygame.Surface((self.width, 30), pygame.SRCALPHA)
        ground.fill((0, 200, 255, 12))
        surf.blit(ground, (0, self.height - 30))

        # Cables (se desvanecen con el progreso)
        fade = max(0.0, 1.0 - self._step * 0.35)
        for wire in self.wires:
            wire.draw(surf, fade)

        # Conexiones limpias entre nodos
        if self.node_stats.visible:
            draw_arrow_line(surf,
                            (self.node_video.x, self.node_video.y),
                            (self.node_stats.x, self.node_stats.y),
                            C_SUCCESS, alpha=int(self.node_stats._appear * 200))
        if self.node_repo.visible:
            draw_arrow_line(surf,
                            (self.node_video.x, self.node_video.y),
                            (self.node_repo.x, self.node_repo.y),
                            C_CYAN, alpha=int(self.node_repo._appear * 200))

        # Nodos
        self.node_video.draw(surf, self.frame)
        self.node_stats.draw(surf, self.frame)
        self.node_repo.draw(surf, self.frame)

        # Labels contextuales
        self._draw_context_labels(surf)

        return surf

    def _draw_context_labels(self, surf: pygame.Surface):
        font = get_font(14, "mono", bold=True)
        if self._step == STEP_CHAOS:
            lines = ["⚠ CLASE SOBRECARGADA", "Demasiadas responsabilidades"]
            color = C_DANGER
            y = self.node_video.y - self.node_video.radius - 52
        elif self._step >= STEP_DONE:
            lines = ["✅ ARQUITECTURA LIMPIA", "Responsabilidades separadas"]
            color = C_SUCCESS
            y = 28
        else:
            return

        # Fondo semiópaco para que el texto se lea sobre cables y fondo
        line_height = 22
        max_w = max(font.size(l)[0] for l in lines)
        pad_x, pad_y = 20, 12
        box_w = max_w + pad_x * 2
        box_h = len(lines) * line_height + pad_y * 2
        box_x = (self.width - box_w) // 2
        box_y = y - pad_y
        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        panel.fill((8, 18, 28, 230))
        pygame.draw.rect(panel, (*color[:3], 120), panel.get_rect(), 2)
        surf.blit(panel, (box_x, box_y))

        for line in lines:
            ts = font.render(line, True, color)
            rx = (self.width - ts.get_width()) // 2
            render_text_with_outline(surf, font, line, color, (rx, y),
                                     outline_color=(5, 10, 15))
            y += line_height

    # Propiedades sincronizadas vía update()
    _state_broken = False
    _step         = STEP_CHAOS

    def update(self, dt: float, state: GameState):   # noqa: F811
        self.frame += 1
        self._update_node_positions()
        self._state_broken = state.broken
        self._step         = state.step

        self.node_stats.visible = state.stats_created
        self.node_repo.visible  = state.repo_created

        if state.broken:
            self.node_video.color = C_DANGER
        elif state.step >= STEP_DONE:
            self.node_video.color = C_SUCCESS
        else:
            self.node_video.color = C_ACCENT

        for wire in self.wires:
            wire.update()
        self.node_video.update(dt)
        self.node_stats.update(dt)
        self.node_repo.update(dt)
