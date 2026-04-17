"""
Panel lateral derecho — pestañas de código + botones de acción.
"""

import pygame
from core.constants import (
    C_DANGER, C_SUCCESS, C_TEXT, C_CYAN, C_DIM, C_ACCENT, C_PANEL,
    C_LINE_NUM, C_BLACK, C_WHITE, C_CODE_TEXT,
    CITY_WIDTH, HEADER_HEIGHT, PANEL_WIDTH, CITY_HEIGHT, STEP_CHAOS,
    STEP_STATS, STEP_REPO, SCREEN_WIDTH
)
from core.fonts import get_font
from core.draw_utils import draw_panel, draw_progress_bar, render_text_with_outline  # noqa: E501
from core.state import GameState
from ui.code_content_srp import CODE_BROKEN, CODE_STATS, CODE_REPO

SYN = {
    "kw": (220, 140, 255),
    "cls": (255, 255, 200),
    "fn": (120, 230, 255),
    "st": (160, 255, 180),
    "cm": (130, 200, 220),
    "num": (255, 180, 100),
    "broken": C_DANGER,
    "fixed": (120, 255, 180),
    "default": C_CODE_TEXT,
}

TABS = ["broken", "stats", "repo"]
TAB_LABELS = {
    "broken": "video.py ⚠",
    "stats": "video_stats.py",
    "repo": "video_repo.py",
}

# Zona fija para barra de progreso (evita que tape el texto de misión)
PROGRESS_BAND_H = 50


def _wrap_text(font: pygame.font.Font, text: str, max_width: int) -> list[str]:
    """Ajusta el texto al ancho máximo; devuelve lista de líneas."""
    if not text.strip():
        return []
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip() if current else word
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Button:
    def __init__(self, rect: pygame.Rect, text: str,
                 action: str, style: str = "normal"):
        self.rect = rect
        self.text: str = text
        self.action: str = action
        self.style: str = style   # 'normal' | 'danger' | 'success'
        self.hovered: bool = False
        self.enabled: bool = True

    @property
    def _colors(self):
        if self.style == "danger":
            return C_DANGER,  (255, 34, 85,  40)
        if self.style == "success":
            return C_SUCCESS, (0, 255, 136, 40)
        return C_CYAN, (0, 255, 255, 40)

    def draw(self, surf: pygame.Surface):
        border, hover_bg = self._colors
        color = border if self.enabled else (*border[:3],)

        bg_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)  # noqa: E501
        if self.hovered and self.enabled:
            bg_surf.fill(hover_bg)
        surf.blit(bg_surf, self.rect.topleft)

        pygame.draw.rect(surf, color, self.rect, 1)

        # Barra lateral izquierda
        bar_h = self.rect.height if (self.hovered and self.enabled) else 4
        pygame.draw.rect(surf, color,
                         pygame.Rect(self.rect.x, self.rect.y, 3, bar_h))

        font = get_font(14, "body", bold=False)
        ts = font.render(self.text, True, color if self.enabled else C_DIM)
        surf.blit(ts, (self.rect.x + 10, self.rect.y + (self.rect.height - ts.get_height()) // 2))  # noqa: E501

    def handle_motion(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def handle_click(self, pos) -> str | None:
        if self.enabled and self.rect.collidepoint(pos):
            return self.action
        return None


class SidePanel:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen: pygame.Surface = screen
        self.state = state
        self.on_action = None     # callback(action: str)
        self.active_tab = "broken"
        self._scroll_y = 0

        ox = CITY_WIDTH
        oy = HEADER_HEIGHT
        pw = PANEL_WIDTH

        # ── Secciones ──
        self._rect_full = pygame.Rect(ox, oy, pw, CITY_HEIGHT)

        # Misión: parte superior fija; banda inferior reservada para progreso
        self._mission_h = 185
        self._mission_rect = pygame.Rect(ox, oy, pw, self._mission_h)

        # Pestañas de código
        self._tab_h = 28
        self._tab_rect = pygame.Rect(ox, oy + self._mission_h, pw, self._tab_h)

        # Área de código (scrollable); 200 px reservados para botones
        self._action_band_h = 200
        self._code_h = CITY_HEIGHT - self._mission_h - self._tab_h - self._action_band_h  # noqa: E501
        self._code_rect = pygame.Rect(ox, oy + self._mission_h + self._tab_h, pw, self._code_h)  # noqa: E501

        # Acciones (botones)
        self._action_y = oy + self._mission_h + self._tab_h + self._code_h
        self._action_h = self._action_band_h

        # Configuración dinámica — puede ser sobreescrita por configure()
        self._tabs = list(TABS)
        self._tab_labels = dict(TAB_LABELS)
        self._code_override: dict | None = None
        self._build_buttons()

    def _build_buttons_from_specs(self, specs: list):
        """Construye botones desde una lista de specs de nivel."""
        ox = CITY_WIDTH + 10
        w = PANEL_WIDTH - 20
        bh, gap = 36, 6
        y0 = self._action_y + 28
        self.buttons = []
        for i, (text, action, style, enabled) in enumerate(specs):
            b = Button(
                pygame.Rect(ox, y0 + i * (bh + gap), w, bh),
                text, action, style,
            )
            b.enabled = enabled
            self.buttons.append(b)

    def _build_buttons(self):
        ox = CITY_WIDTH + 10
        w = PANEL_WIDTH - 20
        bh = 36
        gap = 6
        y0 = self._action_y + 28

        self.buttons: list[Button] = [
            Button(pygame.Rect(ox, y0,          w, bh),
                   "⚠  Simular: Actualizar cálculo (ver qué pasa)",
                   "break", "danger"),
            Button(pygame.Rect(ox, y0 + bh + gap,        w, bh),
                   "✂  Extraer clase VideoStats (cálculo)",
                   "stats", "normal"),
            Button(pygame.Rect(ox, y0 + (bh + gap) * 2,  w, bh),
                   "✂  Extraer clase VideoRepository (persistencia)",
                   "repo", "normal"),
            Button(pygame.Rect(ox, y0 + (bh + gap) * 3,  w, bh),
                   "▶  Aplicar Refactorización → Conectar clases",
                   "finish", "success"),
        ]
        # Estado inicial
        self.buttons[2].enabled = False   # repo bloqueado
        self.buttons[3].enabled = False   # finish bloqueado

    # ── API para niveles ─────────────────────────────────────

    def configure(
            self, tabs: dict, buttons: list,
            code_module: str = None):  # noqa: ARG002
        """Niveles llaman esto en setup() para personalizar el panel."""
        self._tabs = list(tabs.keys())
        self._tab_labels = dict(tabs)
        self.active_tab = self._tabs[0]
        self._build_buttons_from_specs(buttons)

    def set_code_content(self, content: dict):
        """Inyecta contenido de código directamente (tokens por tab)."""
        self._code_override = dict(content)

    def set_tab_by_index(self, idx: int):
        if 0 <= idx < len(self._tabs):
            self.set_tab(self._tabs[idx])

    def set_tab(self, name: str):
        if name in self._tabs:
            self.active_tab = name
            self._scroll_y = 0

    def update(self, dt: float):  # noqa: ARG001
        """Actualización por frame. El estado de los botones lo sincroniza el nivel."""  # noqa: E501
        pass

    def handle_click(self, pos):
        # Pestañas
        if self._tab_rect.collidepoint(pos):
            tab_w = PANEL_WIDTH // len(self._tabs)
            idx = (pos[0] - CITY_WIDTH) // tab_w
            if 0 <= idx < len(self._tabs):
                self.set_tab(self._tabs[idx])
            return

        # Clic en área de código: scroll proporcional (para ver todo el código)
        if self._code_rect.collidepoint(pos):
            content_h = self._get_code_content_height()
            if content_h > self._code_h:
                rel_y = (pos[1] - self._code_rect.y) / self._code_rect.h
                self._scroll_y = int(rel_y * (content_h - self._code_h))
                self._scroll_y = max(0, min(content_h - self._code_h, self._scroll_y))  # noqa: E501
            return

        # Botones
        for btn in self.buttons:
            action = btn.handle_click(pos)
            if action and self.on_action:
                self.on_action(action)

    def handle_motion(self, pos):
        for btn in self.buttons:
            btn.handle_motion(pos)

    # ──────────────────────────────────────────
    # Dibujo
    # ──────────────────────────────────────────
    def draw(self):
        s = self.screen
        ox, oy = CITY_WIDTH, HEADER_HEIGHT

        # Fondo del panel
        draw_panel(s, self._rect_full, bg=C_PANEL, border=C_DIM, alpha=200, border_w=0)  # noqa: E501

        self._draw_mission(s, ox, oy)
        self._draw_tabs(s)
        self._draw_code(s)
        self._draw_actions(s)

    def _draw_mission(self, surf, ox, oy):
        font_tag = get_font(11, "mono")
        font_body = get_font(12, "body")

        # Etiqueta SRP
        # Mostrar el nombre del principio/nivel, usando un font más grande y generado según el nivel. # noqa: E501
        level_name = getattr(self.state, "level_name", "PRINCIPIO S.R.P.")  # o equiv. # noqa: E501
        font_level = get_font(20, "mono", bold=True)
        tag = font_level.render(level_name, True, C_ACCENT)
        surf.blit(tag, (ox + 14, oy + 10))
        pygame.draw.rect(surf, C_ACCENT,
                         pygame.Rect(ox + 10, oy + 8, tag.get_width() + 8, 22), 1)  # noqa: E501

        # Título sección
        level_title = getattr(self.state, "level_title", "MISIÓN ACTUAL")
        font_title = get_font(16, "mono", bold=False)
        title = font_title.render(level_title, True, C_CYAN)
        surf.blit(title, (ox + 14, oy + 36))
        pygame.draw.line(surf, C_DIM,
                         (ox + 10, oy + 54), (ox + PANEL_WIDTH - 10, oy + 54), 1)  # noqa: E501

        # Texto de misión según paso (párrafos para envolver)
        st = self.state
        if st.step == STEP_CHAOS and not st.broken:
            raw = [
                "La clase Video intenta hacer DOS cosas: calcular estadísticas "  # noqa: E501
                "Y guardar en la base de datos.",
                "",
                "Usá la herramienta de refactorización para separar "
                "responsabilidades.",
            ]
            body_color = C_TEXT
        elif st.broken:
            raw = [
                "¡La base de datos se rompió al actualizar el cálculo! Ambas "
                "responsabilidades están acopladas.",
                "",
                "Separalas para estabilizar el sistema.",
            ]
            body_color = C_DANGER
        elif st.step == STEP_STATS:
            raw = [
                "VideoStats creada ✅ Ahora extraé VideoRepository para "
                "separar la persistencia de la lógica de cálculo.",
            ]
            body_color = C_TEXT
        elif st.step == STEP_REPO:
            raw = [
                "VideoRepository creada ✅ Ambas clases independientes. "
                "¡Conectalas para completar el refactoring!",
            ]
            body_color = C_TEXT
        else:
            raw = [
                "✅ ¡Refactorización completa! La ciudad está estabilizada.",
            ]
            body_color = C_SUCCESS

        max_text_w = PANEL_WIDTH - 28
        lines = []
        for block in raw:
            if block:
                lines.extend(_wrap_text(font_body, block, max_text_w))
            else:
                lines.append("")

        # Zona de texto: arriba de la banda de progreso (no solapa)
        body_top = oy + 60
        body_bottom = oy + self._mission_h - PROGRESS_BAND_H
        line_height = 18
        y = body_top
        clip_rect = pygame.Rect(ox, body_top, PANEL_WIDTH, body_bottom - body_top)  # noqa: E501
        surf.set_clip(clip_rect)
        for line in lines:
            if y + line_height <= body_bottom:
                if line:
                    ts = font_body.render(line, True, body_color)
                    surf.blit(ts, (ox + 14, y))
                y += line_height
        surf.set_clip(None)

        # Banda de progreso fija abajo (siempre visible, no tapa texto)
        prog_y = oy + self._mission_h - PROGRESS_BAND_H
        pct_label = font_tag.render(
            f"PROGRESO  {int(self.state.progress_pct*100)}%", True, C_TEXT
        )
        surf.blit(pct_label, (ox + 14, prog_y + 8))
        pr_rect = pygame.Rect(ox + 14, prog_y + 28, PANEL_WIDTH - 28, 8)
        draw_progress_bar(surf, pr_rect, self.state.progress_pct, C_SUCCESS)
        pygame.draw.line(surf, C_DIM,
                         (ox, oy + self._mission_h - 1),
                         (ox + PANEL_WIDTH, oy + self._mission_h - 1), 1)

    def _draw_tabs(self, surf):
        tab_w = PANEL_WIDTH // len(self._tabs)
        oy = HEADER_HEIGHT + self._mission_h
        ox = CITY_WIDTH
        font = get_font(11, "mono")

        for i, tab in enumerate(self._tabs):
            tx = ox + i * tab_w
            # rect = pygame.Rect(tx, oy, tab_w, self._tab_h)
            active = tab == self.active_tab

            if active:
                pygame.draw.rect(surf, (0, 255, 255, 20),
                                 pygame.Rect(tx, oy, tab_w, self._tab_h))
                pygame.draw.line(surf, C_CYAN,
                                 (tx, oy + self._tab_h - 2),
                                 (tx + tab_w, oy + self._tab_h - 2), 2)
                color = C_BLACK  # texto legible sobre fondo cyan
            else:
                color = C_WHITE  # pestaña no seleccionada: color normal, letras blancas  # noqa: E501 

            label = self._tab_labels.get(tab, tab)
            ts = font.render(label, True, color)
            surf.blit(ts, (tx + (tab_w - ts.get_width()) // 2,
                           oy + (self._tab_h - ts.get_height()) // 2))

        pygame.draw.line(surf, C_DIM,
                         (ox, oy + self._tab_h),
                         (ox + PANEL_WIDTH, oy + self._tab_h), 1)

    def _get_code_lines(self):
        """Devuelve las líneas de código de la pestaña activa (para dibujo y scroll)."""  # noqa: E501
        _default = {
            "broken": CODE_BROKEN,
            "stats":  CODE_STATS,
            "repo":   CODE_REPO,
        }
        src = self._code_override or _default
        return src.get(self.active_tab, [])

    def _get_code_content_height(self):
        """Altura total en píxeles del contenido de código (para límite de scroll)."""  # noqa: E501
        lines = self._get_code_lines()
        lh = 22
        return len(lines) * lh + 12  # 6 arriba + 6 abajo

    def handle_wheel(self, pos, dy: int):
        """Scroll del área de código cuando el puntero está sobre ella. dy > 0 = scroll arriba."""  # noqa: E501
        if not self._code_rect.collidepoint(pos):
            return
        content_h = self._get_code_content_height()
        max_scroll = max(0, content_h - self._code_h)
        step = 22  # 1 línea por vuelta de rueda
        self._scroll_y = max(0, min(max_scroll, self._scroll_y + dy * step))

    def _draw_code(self, surf):
        lines = self._get_code_lines()
        lh = 22
        content_h = max(self._code_h, len(lines) * lh + 12)

        # Superficie con todo el contenido (puede ser más alta que el área visible)  # noqa: E501
        code_surf = pygame.Surface((PANEL_WIDTH, content_h), pygame.SRCALPHA)
        code_surf.fill((6, 13, 20, 240))

        font_code = get_font(15, "mono", bold=False)
        font_code_bold = get_font(15, "mono", bold=True)
        font_ln = get_font(13, "mono")
        y = 6

        for i, (tokens, is_broken_line) in enumerate(lines):
            ln_ts = font_ln.render(f"{i+1:2}", True, C_LINE_NUM)
            code_surf.blit(ln_ts, (4, y))
            x = 36
            for text, style in tokens:
                color = SYN.get(style, SYN["default"])
                font = font_code_bold if style in ("cls", "fixed") else font_code  # noqa: E501
                render_text_with_outline(code_surf, font, text, color, (x, y),
                                         outline_color=(2, 8, 12))
                x += font.size(text)[0]
            y += lh

        # Recortar y blit solo la ventana visible (deslizable)
        dest_y = HEADER_HEIGHT + self._mission_h + self._tab_h
        dest_rect = pygame.Rect(CITY_WIDTH, dest_y, PANEL_WIDTH, self._code_h)
        src_rect = (0, self._scroll_y, PANEL_WIDTH, self._code_h)
        surf.blit(code_surf, dest_rect, src_rect)

        # Barra de scroll visible cuando el contenido es más alto que el área
        if content_h > self._code_h:
            sb_x = CITY_WIDTH + PANEL_WIDTH - 10
            sb_y = dest_y
            track_rect = pygame.Rect(sb_x, sb_y, 6, self._code_h)
            pygame.draw.rect(surf, C_DIM, track_rect, border_radius=3)
            visible_ratio = self._code_h / content_h
            thumb_h = max(24, int(self._code_h * visible_ratio))
            max_scroll = content_h - self._code_h
            thumb_y = sb_y + int((self._code_h - thumb_h) * self._scroll_y
                                 / max_scroll) if max_scroll > 0 else sb_y
            thumb_rect = pygame.Rect(sb_x + 1, thumb_y, 4, thumb_h)
            pygame.draw.rect(surf, C_CYAN, thumb_rect, border_radius=2)

        # Borde inferior
        pygame.draw.line(surf, C_DIM,
                         (CITY_WIDTH, HEADER_HEIGHT + self._mission_h + self._tab_h + self._code_h),  # noqa: E501
                         (SCREEN_WIDTH, HEADER_HEIGHT + self._mission_h + self._tab_h + self._code_h), 1)  # noqa: E501

    def _draw_actions(self, surf):
        ay = self._action_y
        font = get_font(12, "mono", bold=True)

        title_ts = font.render("⚡  HERRAMIENTAS DE REFACTORIZACIÓN", True, C_ACCENT)  # noqa: E501
        surf.blit(title_ts, (CITY_WIDTH + 10, ay + 8))

        for btn in self.buttons:
            btn.draw(surf)
