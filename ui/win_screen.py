"""
Pantalla de victoria — resumen de lo aprendido.
v2: soporte para botón "Siguiente Nivel" cuando hay más niveles disponibles.
"""

import pygame
import math
from core.constants import *
from core.fonts import get_font
from core.draw_utils import draw_panel
from core.state import GameState

LESSONS = {
    1: [
        "Una clase debe tener UNA SOLA razón para cambiar.",
        "VideoStats solo cambia si la lógica de cálculo cambia.",
        "VideoRepository solo cambia si la base de datos cambia.",
        "Podés cambiar una parte sin romper la otra.",
        "El código SRP es más fácil de testear y mantener.",
    ],
    2: [
        "Las clases deben estar ABIERTAS para extensión...",
        "...pero CERRADAS para modificación.",
        "Cada nuevo tipo es una clase nueva, no un if/elif más.",
        "DiscountCalculator nunca se toca para agregar descuentos.",
        "Extender sin modificar = cero riesgo de regresión.",
    ],
}


class WinScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.visible = False
        self._frame  = 0
        self._btn_next    = pygame.Rect(0, 0, 200, 48)
        self._btn_restart = pygame.Rect(0, 0, 200, 48)
        self._btn_menu    = pygame.Rect(0, 0, 160, 48)
        self._has_next    = False  # actualizado en draw(); usado en handle_click

    def handle_click(self, pos) -> str | None:
        if self._has_next and self._btn_next.collidepoint(pos):
            return "next"
        if self._btn_restart.collidepoint(pos):
            return "restart"
        if self._btn_menu.collidepoint(pos):
            return "menu"
        return None

    def draw(self, state: GameState, level_index: int = 0, total_levels: int = 1):
        self._frame += 1
        s  = self.screen
        cx = SCREEN_WIDTH // 2

        # Fondo
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        bg.fill((2, 5, 10, 240))
        s.blit(bg, (0, 0))

        pulse = math.sin(self._frame * 0.06) * 8

        # Título
        font_big = get_font(46, "title", bold=True)
        t1 = font_big.render("NIVEL COMPLETADO", True, C_SUCCESS)
        s.blit(t1, (cx - t1.get_width() // 2, 40))

        # Subtítulo del principio
        principles = {0: "S.R.P. — SINGLE RESPONSIBILITY", 1: "O.C.P. — OPEN/CLOSED PRINCIPLE"}
        subtitle = principles.get(level_index, "PRINCIPIO DOMINADO")
        font_sub = get_font(12, "mono")
        sub = font_sub.render(subtitle + "  DOMINADO", True, C_ACCENT)
        s.blit(sub, (cx - sub.get_width() // 2, 100))

        # Puntaje
        font_score = get_font(int(56 + pulse), "title", bold=True)
        sc = font_score.render(str(state.score), True, C_ACCENT)
        s.blit(sc, (cx - sc.get_width() // 2, 120))
        sl = font_sub.render("PUNTOS DE MANTENIBILIDAD", True, C_DIM)
        s.blit(sl, (cx - sl.get_width() // 2, 190))

        # Lecciones
        lessons = LESSONS.get(level_index + 1, [])
        box_w, box_h = 640, 180
        box_rect = pygame.Rect(cx - box_w // 2, 215, box_w, box_h)
        draw_panel(s, box_rect, bg=(0, 30, 20), border=C_SUCCESS, alpha=180)
        font_lh = get_font(11, "mono", bold=True)
        lh_ts   = font_lh.render("📚  LO QUE APRENDISTE", True, C_SUCCESS)
        s.blit(lh_ts, (cx - lh_ts.get_width() // 2, 222))
        pygame.draw.line(s, (*C_SUCCESS, 80),
                         (cx - box_w // 2 + 20, 240),
                         (cx + box_w // 2 - 20, 240), 1)
        font_les = get_font(12, "body")
        y = 248
        for lesson in lessons:
            arrow = font_les.render("▸", True, C_SUCCESS)
            text  = font_les.render(lesson, True, C_TEXT)
            s.blit(arrow, (cx - box_w // 2 + 18, y))
            s.blit(text,  (cx - box_w // 2 + 36, y))
            y += 22

        # Botones: tres botones en fila
        self._has_next = level_index < total_levels - 1
        mouse = pygame.mouse.get_pos()
        by = SCREEN_HEIGHT - 88
        bw, bh = 200, 48
        bm, _ = self._btn_menu.size
        cx = SCREEN_WIDTH // 2
        gap = 16

        # Siempre mostrar "Menú" a la derecha
        self._btn_menu.x = cx + bw + gap
        self._btn_menu.y = by
        self._btn_menu.w = 160
        self._btn_menu.h = bh
        self._draw_btn(s, self._btn_menu, "☰  MENÚ", C_DIM, mouse)

        if self._has_next:
            # Tres botones: Siguiente nivel, Jugar de nuevo, Menú
            total_w = bw * 2 + gap + 160 + gap
            left_x = cx - total_w // 2
            self._btn_next.x = left_x
            self._btn_next.y = by
            self._btn_next.w = bw
            self._btn_next.h = bh
            self._btn_restart.x = left_x + bw + gap
            self._btn_restart.y = by
            self._btn_restart.w = bw
            self._btn_restart.h = bh
            self._draw_btn(s, self._btn_next, "▶  SIGUIENTE", C_SUCCESS, mouse)
            self._draw_btn(s, self._btn_restart, "↺  REINICIAR", C_DIM, mouse)
        else:
            # Dos botones: Jugar de nuevo (izq.) y Menú (der.)
            self._btn_restart.x = cx - bw - gap // 2
            self._btn_restart.y = by
            self._btn_restart.w = bw
            self._btn_restart.h = bh
            self._draw_btn(s, self._btn_restart, "↺  REINICIAR", C_CYAN, mouse)

    def _draw_btn(self, surf, rect, label, color, mouse):
        hovered = rect.collidepoint(mouse)
        bg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg.fill((*color, 40 if hovered else 10))
        surf.blit(bg, rect.topleft)
        pygame.draw.rect(surf, color, rect, 1)
        font = get_font(12, "mono", bold=True)
        ts   = font.render(label, True, color)
        surf.blit(ts, (rect.centerx - ts.get_width() // 2,
                       rect.centery - ts.get_height() // 2))
