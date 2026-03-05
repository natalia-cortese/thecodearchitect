"""
Overlay de feedback — modal semitransparente con animación.
"""

import pygame
from core.constants import *
from core.fonts import get_font
from core.draw_utils import draw_panel


class FeedbackOverlay:
    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.visible = False
        self._kind   = "success"
        self._title  = ""
        self._body   = []
        self._btn    = ""
        self._anim   = 0.0   # 0→1 aparición

        # Botón OK
        bw, bh = 300, 40
        cx = SCREEN_WIDTH  // 2
        self._btn_rect = pygame.Rect(cx - bw // 2, 0, bw, bh)   # y se calcula al dibujar

    def show(self, kind: str, title: str, body: list[str], btn_text: str = "CONTINUAR"):
        self._kind   = kind
        self._title  = title
        self._body   = body
        self._btn    = btn_text
        self.visible = True
        self._anim   = 0.0

    def hide(self):
        self.visible = False

    def update(self, dt: float):
        if self.visible and self._anim < 1.0:
            self._anim = min(1.0, self._anim + dt * 4)

    def handle_click(self, pos):
        if self.visible and self._btn_rect.collidepoint(pos):
            self.hide()

    def draw(self):
        s = self.screen

        # Fondo oscuro
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, int(180 * self._anim)))
        s.blit(dim, (0, 0))

        if self._anim < 0.05:
            return

        # Caja central
        box_w, box_h = 540, 360
        bx = SCREEN_WIDTH  // 2 - box_w // 2
        by = SCREEN_HEIGHT // 2 - box_h // 2 - int((1 - self._anim) * 20)
        box_rect = pygame.Rect(bx, by, box_w, box_h)

        color = C_SUCCESS if self._kind == "success" else C_DANGER
        draw_panel(s, box_rect, bg=C_PANEL, border=color, alpha=230, border_w=2)

        # Icono
        icon    = "✅" if self._kind == "success" else "⚠"
        font_ic = get_font(36, "body")
        ic_ts   = font_ic.render(icon, True, color)
        s.blit(ic_ts, (bx + box_w // 2 - ic_ts.get_width() // 2, by + 20))

        # Título
        font_t = get_font(18, "title", bold=True)
        t_ts   = font_t.render(self._title, True, color)
        s.blit(t_ts, (bx + box_w // 2 - t_ts.get_width() // 2, by + 72))
        pygame.draw.line(s, (*color, 100),
                         (bx + 30, by + 100), (bx + box_w - 30, by + 100), 1)

        # Cuerpo
        font_b = get_font(13, "body")
        y      = by + 112
        for line in self._body:
            if line:
                ts = font_b.render(line, True, C_TEXT)
                s.blit(ts, (bx + box_w // 2 - ts.get_width() // 2, y))
            y += 18

        # Botón
        bw, bh = 300, 40
        btn_y  = by + box_h - 56
        self._btn_rect = pygame.Rect(bx + box_w // 2 - bw // 2, btn_y, bw, bh)

        hovered = self._btn_rect.collidepoint(pygame.mouse.get_pos())
        bg_a    = 40 if hovered else 0
        btn_bg  = pygame.Surface((bw, bh), pygame.SRCALPHA)
        btn_bg.fill((*color, bg_a))
        s.blit(btn_bg, self._btn_rect.topleft)
        pygame.draw.rect(s, color, self._btn_rect, 1)

        font_btn = get_font(11, "mono", bold=True)
        btn_ts   = font_btn.render(self._btn, True, color)
        s.blit(btn_ts, (self._btn_rect.centerx - btn_ts.get_width() // 2,
                        self._btn_rect.centery - btn_ts.get_height() // 2))
