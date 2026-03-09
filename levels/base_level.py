"""
BaseLevel — interfaz que todo nivel debe implementar.
game.py solo habla con esta interfaz; nunca con niveles concretos.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.state import GameState
    from ui.panel import SidePanel
    from ui.feedback import FeedbackOverlay
    from ui.win_screen import WinScreen


class BaseLevel:
    # Metadatos que cada nivel declara
    level_number: int  = 0
    title:        str  = ""
    subtitle:     str  = ""
    principle:    str  = ""

    def setup(self, state: "GameState", panel: "SidePanel",
              overlay: "FeedbackOverlay", win: "WinScreen") -> None:
        """Llamado una vez al iniciar el nivel. Configurá tabs, botones, estado."""
        raise NotImplementedError

    def handle_action(self, action: str) -> None:
        """Recibe los action IDs que disparan los botones del panel."""
        raise NotImplementedError

    def update_panel_buttons(self, state: "GameState") -> None:
        """Sincroniza el estado enabled de los botones con el estado del nivel."""
        pass

