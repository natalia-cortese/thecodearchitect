"""
Estado mutable del juego — única fuente de verdad.
"""

from core.constants import STEP_CHAOS


class GameState:
    def __init__(self):
        self.step:            int  = STEP_CHAOS
        self.score:           int  = 0
        self.maintainability: int  = 0    # 0-100
        self.stability:       int  = 100  # 0-100
        self.stats_created:   bool = False
        self.repo_created:    bool = False
        self.broken:          bool = False

    def add_score(self, pts: int):
        self.score += pts

    @property
    def progress_pct(self) -> float:
        """Porcentaje de progreso del nivel (0.0–1.0)."""
        return self.step / 3.0
