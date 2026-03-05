"""
Bucle principal del juego — orquesta escenas y estado global.
Cambios respecto a v1: las acciones se delegan al nivel activo (self.level).
"""

import pygame
from core.constants import *
from core.state import GameState
from ui.hud import HUD
from ui.panel import SidePanel
from ui.feedback import FeedbackOverlay
from ui.win_screen import WinScreen
from levels.city_view import CityView
from levels.srp_level import SRPLevel
from levels.ocp_level import OCPLevel

LEVELS = [SRPLevel, OCPLevel]


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 start_level: int = 1):
        self.screen      = screen
        self.clock       = clock
        self.level_index = start_level - 1   # 0-based
        self._init_level()

    def _init_level(self):
        """Inicializa (o reinicia) el nivel actual."""
        self.state   = GameState()
        self.city    = CityView(CITY_WIDTH, CITY_HEIGHT)
        self.hud     = HUD(self.screen)
        self.panel   = SidePanel(self.screen, self.state)
        self.overlay = FeedbackOverlay(self.screen)
        self.win     = WinScreen(self.screen)

        # Instanciar y configurar el nivel activo
        self.level = LEVELS[self.level_index]()
        self.level.setup(self.state, self.panel, self.overlay, self.win)

        # Sobreescribir título del HUD con los metadatos del nivel
        self.hud.title    = self.level.title
        self.hud.subtitle = self.level.subtitle

        # Conectar callback
        self.panel.on_action = self.level.handle_action

    # ──────────────────────────────────────────
    # Bucle principal
    # ──────────────────────────────────────────
    def run(self):
        """Bucle bloqueante para uso desktop (sin Pygbag)."""
        while self.tick():
            pass

    def tick(self) -> bool:
        """Procesa un frame. Retorna False cuando el juego debe cerrar.

        Separado de run() para compatibilidad con el loop asíncrono
        de Pygbag (WebAssembly).
        """
        dt = self.clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.overlay.visible:
                        self.overlay.hide()
                    elif self.win.visible:
                        self._next_or_restart()
                    else:
                        return False

                if not self.overlay.visible and not self.win.visible:
                    if event.key == pygame.K_1:
                        self.panel.set_tab_by_index(0)
                    elif event.key == pygame.K_2:
                        self.panel.set_tab_by_index(1)
                    elif event.key == pygame.K_3:
                        self.panel.set_tab_by_index(2)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.win.visible:
                    action = self.win.handle_click(event.pos)
                    if action == "next":
                        self._advance_level()
                    elif action == "restart":
                        self._init_level()
                elif self.overlay.visible:
                    self.overlay.handle_click(event.pos)
                else:
                    self.panel.handle_click(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if not self.overlay.visible and not self.win.visible:
                    self.panel.handle_motion(event.pos)

        # ── Update ──
        self.city.update(dt, self.state)
        self.panel.update(dt)
        self.overlay.update(dt)

        # ── Draw ──
        self.screen.fill(C_BG)
        self._draw_grid()
        city_surf = self.city.draw()
        self.screen.blit(city_surf, (0, HEADER_HEIGHT))
        self.hud.draw(self.state)
        self.panel.draw()
        pygame.draw.line(self.screen, C_DIM,
                         (CITY_WIDTH, HEADER_HEIGHT),
                         (CITY_WIDTH, SCREEN_HEIGHT), 1)
        if self.overlay.visible:
            self.overlay.draw()
        if self.win.visible:
            self.win.draw(self.state, self.level_index, len(LEVELS))

        pygame.display.flip()
        return True

    # ──────────────────────────────────────────
    def _draw_grid(self):
        grid_surf = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        color = (0, 255, 255, 8)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(grid_surf, color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(grid_surf, color, (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(grid_surf, (0, 0))

    def _advance_level(self):
        if self.level_index < len(LEVELS) - 1:
            self.level_index += 1
            self._init_level()

    def _next_or_restart(self):
        if self.level_index < len(LEVELS) - 1:
            self._advance_level()
        else:
            self._init_level()
