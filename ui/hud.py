"""
HUD — barra superior con título y estadísticas del jugador.
"""

import pygame
import math
from core.constants import *
from core.fonts import get_font
from core.draw_utils import draw_panel
from core.state import GameState


class HUD:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.rect   = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
        self._score_anim = 0.0   # escala de animación de puntos

    title    = "THE CODE ARCHITECT"
    subtitle = "NIVEL 01  //  SRP — SINGLE RESPONSIBILITY PRINCIPLE"

    def draw(self, state: GameState):
        s = self.screen

        # Fondo semitransparente
        draw_panel(s, self.rect, bg=C_BG, border=C_DIM, alpha=220, border_w=0)
        pygame.draw.line(s, C_DIM, (0, HEADER_HEIGHT - 1), (SCREEN_WIDTH, HEADER_HEIGHT - 1), 1)

        # ── Título ──
        font_title = get_font(20, "title", bold=True)
        font_sub   = get_font(10, "mono")

        parts = self.title.split()
        t1 = font_title.render(parts[0], True, C_CYAN)
        t2 = font_title.render(" ".join(parts[1:]) if len(parts) > 1 else "", True, C_ACCENT)
        s.blit(t1, (24, 10))
        s.blit(t2, (24 + t1.get_width() + 8, 10))

        sub = font_sub.render(self.subtitle, True,
                              (C_CYAN[0], C_CYAN[1], C_CYAN[2]))
        sub_s = pygame.Surface(sub.get_size(), pygame.SRCALPHA)
        sub_s.blit(sub, (0, 0))
        sub_s.set_alpha(130)
        s.blit(sub_s, (26, 38))

        # ── Stats ──
        stats = [
            ("MANTENIBILIDAD", state.maintainability,  self._maint_color(state.maintainability)),
            ("ESTABILIDAD",    state.stability,         self._stab_color(state.stability)),
            ("PUNTOS",         state.score,             C_ACCENT),
        ]
        sx = SCREEN_WIDTH - 320
        for label, value, color in stats:
            self._draw_stat(s, sx, label, str(value), color)
            sx += 110

    def _draw_stat(self, surf, x, label, value, color):
        lf  = get_font(9,  "mono")
        vf  = get_font(22, "title", bold=True)
        lts = lf.render(label, True, (C_TEXT[0], C_TEXT[1], C_TEXT[2]))
        vts = vf.render(value, True, color)
        # Glow bajo el número
        glow = pygame.Surface((vts.get_width() + 10, vts.get_height() + 6), pygame.SRCALPHA)
        glow.fill((*color, 20))
        surf.blit(glow, (x - 5, 30))
        surf.blit(lts, (x, 12))
        surf.blit(vts, (x, 28))

    @staticmethod
    def _maint_color(v):
        if v > 60: return C_SUCCESS
        if v > 30: return C_ACCENT
        return C_DANGER

    @staticmethod
    def _stab_color(v):
        if v > 60: return C_SUCCESS
        if v > 30: return C_ACCENT
        return C_DANGER
