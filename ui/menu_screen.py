"""
Pantalla de menú principal — login de jugador y selección de nivel.
"""

import pygame
from core.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, C_BG, C_PANEL, C_CYAN,
    C_ACCENT, C_DANGER, C_SUCCESS, C_DIM, C_TEXT, C_WHITE,
)
from core.fonts import get_font


LEVEL_COLORS = {
    0: C_CYAN,
    1: (0, 200, 255),
    2: (180, 100, 255),
    3: C_ACCENT,
}


class MenuScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.visible = True

        from core.player import PlayerManager
        self.player_manager = PlayerManager.get_instance()

        self._input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 280, 300, 50)
        self._btn_login_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 45)

        self._input_text = ""
        self._input_active = False
        self._error_msg = ""
        self._selected_level = None

        self._create_level_buttons()

    def _create_level_buttons(self):
        from core.game import LEVELS
        y_start = 180
        for i, level_cls in enumerate(LEVELS):
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_start + i * 70, 400, 60)
            self._level_buttons.append({
                "rect": btn,
                "level_index": i,
                "level": level_cls,
            })

    def handle_event(self, event: pygame.event.Event) -> int | None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if self._input_rect.collidepoint(pos):
                self._input_active = True
            else:
                self._input_active = False
                if self._btn_login_rect.collidepoint(pos):
                    return self._try_login()

            for btn_data in self._level_buttons:
                if btn_data["rect"].collidepoint(pos):
                    player = self.player_manager.get_current_player()
                    if player:
                        self._selected_level = btn_data["level_index"]
                        return btn_data["level_index"]
                    else:
                        self._error_msg = "Primero ingresa tu nombre"

        elif event.type == pygame.KEYDOWN:
            if self._input_active:
                if event.key == pygame.K_BACKSPACE:
                    self._input_text = self._input_text[:-1]
                    self._error_msg = ""
                elif event.key == pygame.K_RETURN:
                    return self._try_login()
                elif len(self._input_text) < 20:
                    if event.unicode.isalnum() or event.unicode in "_- ":
                        self._input_text += event.unicode
                        self._error_msg = ""

        return None

    def _try_login(self) -> int | None:
        name = self._input_text.strip()
        if not name:
            self._error_msg = "Ingresá tu nombre"
            return None

        try:
            self.player_manager.create_player(name)
            self._input_text = ""
            self._error_msg = ""
            return None
        except ValueError as e:
            self._error_msg = str(e)
            return None

    def draw(self):
        s = self.screen
        s.fill(C_BG)

        self._draw_title(s)
        self._draw_login(s)
        self._draw_level_buttons(s)
        self._draw_leaderboard(s)

    def _draw_title(self, s):
        font_title = get_font(48, "title")
        font_sub = get_font(14, "mono")

        title = font_title.render("THE CODE ARCHITECT", True, C_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        s.blit(title, title_rect)

        sub = font_sub.render("Aprendé los principios SOLID jugando", True, C_DIM)
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, 85))
        s.blit(sub, sub_rect)

    def _draw_login(self, s):
        player = self.player_manager.get_current_player()

        if player:
            font_name = get_font(22, "mono")
            font_score = get_font(14, "mono")

            name_surf = font_name.render(f"Player: {player.name}", True, C_SUCCESS)
            name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, 140))
            s.blit(name_surf, name_rect)

            score_surf = font_score.render(
                f"Score: {player.total_score}", True, C_ACCENT
            )
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 165))
            s.blit(score_surf, score_rect)
        else:
            font_label = get_font(12, "mono")
            label = font_label.render("TU NOMBRE", True, C_DIM)
            label_rect = label.get_rect(center=(SCREEN_WIDTH // 2 - 75, 255))
            s.blit(label, label_rect)

            pygame.draw.rect(s, C_PANEL, self._input_rect, border_radius=8)
            pygame.draw.rect(
                s, C_CYAN if self._input_active else C_DIM,
                self._input_rect, 2, border_radius=8
            )

            font_input = get_font(20, "mono")
            input_surf = font_input.render(self._input_text, True, C_WHITE)
            s.blit(input_surf, (self._input_rect.x + 10, self._input_rect.y + 12))

            pygame.draw.rect(s, C_CYAN, self._btn_login_rect, border_radius=6)
            font_btn = get_font(14, "mono")
            btn_text = font_btn.render("JUGAR", True, C_BG)
            btn_rect = btn_text.get_rect(center=self._btn_login_rect.center)
            s.blit(btn_text, btn_rect)

            if self._error_msg:
                font_err = get_font(11, "mono")
                err_surf = font_err.render(self._error_msg, True, C_DANGER)
                err_rect = err_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, self._btn_login_rect.bottom + 18)
                )
                s.blit(err_surf, err_rect)

    def _draw_level_buttons(self, s):
        player = self.player_manager.get_current_player()
        mouse_pos = pygame.mouse.get_pos()

        font_title = get_font(14, "mono")
        title = font_title.render("ELEGÍ UN NIVEL:", True, C_DIM)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 125))
        s.blit(title, title_rect)

        from core.game import LEVELS
        for i, btn_data in enumerate(self._level_buttons):
            level_cls = btn_data["level"]
            color = LEVEL_COLORS.get(i, C_CYAN)

            is_hovered = btn_data["rect"].collidepoint(mouse_pos)
            enabled = player is not None

            if enabled:
                bg_color = C_PANEL if not is_hovered else (20, 40, 30)
                border_color = color if is_hovered else C_DIM
                text_color = C_WHITE
            else:
                bg_color = (10, 15, 20)
                border_color = (30, 40, 50)
                text_color = (80, 90, 100)

            pygame.draw.rect(s, bg_color, btn_data["rect"], border_radius=8)
            pygame.draw.rect(
                s, border_color,
                btn_data["rect"], 2, border_radius=8
            )

            letter_font = get_font(28, "title")
            letter = letter_font.render(level_cls.principle[0], True, text_color)
            letter_rect = letter.get_rect(
                center=(btn_data["rect"].x + 35, btn_data["rect"].centery)
            )
            s.blit(letter, letter_rect)

            name_font = get_font(14, "mono")
            name_surf = name_font.render(level_cls.principle, True, text_color)
            name_rect = name_surf.get_rect(
                midleft=(btn_data["rect"].x + 70, btn_data["rect"].centery)
            )
            s.blit(name_surf, name_rect)

            desc_font = get_font(11, "mono")
            desc = f"Nivel {level_cls.level_number}"
            desc_surf = desc_font.render(desc, True, (60, 70, 80))
            desc_rect = desc_surf.get_rect(
                midleft=(btn_data["rect"].x + 70, btn_data["rect"].centery + 16)
            )
            s.blit(desc_surf, desc_rect)

            if player:
                level_id = level_cls.principle.lower().replace(".", "")
                score = player.get_score(level_id)
                if score > 0:
                    score_font = get_font(12, "mono")
                    score_surf = score_font.render(f"{score} pts", True, C_SUCCESS)
                    score_rect = score_surf.get_rect(
                        midright=(
                            btn_data["rect"].right - 15,
                            btn_data["rect"].centery
                        )
                    )
                    s.blit(score_surf, score_rect)

    def _draw_leaderboard(self, s):
        font_title = get_font(12, "mono")
        title = font_title.render("TOP JUGADORES", True, C_DIM)
        s.blit(title, (20, 20))

        leaderboard = self.player_manager.get_leaderboard()[:5]
        font_name = get_font(12, "mono")

        for i, player in enumerate(leaderboard):
            y = 45 + i * 22
            color = C_ACCENT if i == 0 else C_TEXT
            name_surf = font_name.render(
                f"#{i+1} {player.name}", True, color
            )
            s.blit(name_surf, (20, y))

            score_surf = font_name.render(
                f"{player.total_score}", True, C_DIM
            )
            s.blit(score_surf, (130, y))

    def is_ready(self) -> bool:
        return self.player_manager.get_current_player() is not None
