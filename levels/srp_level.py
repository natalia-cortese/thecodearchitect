"""
Nivel 1 — Single Responsibility Principle (SRP)
Toda la lógica de acciones del nivel 1 encapsulada aquí.
"""

from levels.base_level import BaseLevel
from core.constants import *


class SRPLevel(BaseLevel):
    level_number = 1
    title        = "THE CODE ARCHITECT"
    subtitle     = "NIVEL 01  //  SRP — SINGLE RESPONSIBILITY PRINCIPLE"
    principle    = "S.R.P."

    def setup(self, state, panel, overlay, win):
        self.state   = state
        self.panel   = panel
        self.overlay = overlay
        self.win     = win

        # Tabs y botones específicos de este nivel
        panel.configure(
            tabs={
                "broken": "video.py ⚠",
                "stats":  "video_stats.py",
                "repo":   "video_repo.py",
            },
            buttons=[
                (
                    "⚠  Simular: Actualizar cálculo (ver qué pasa)",
                    "break", "danger", True,
                ),
                (
                    "✂  Extraer clase VideoStats (cálculo)",
                    "stats", "normal", True,
                ),
                (
                    "✂  Extraer clase VideoRepository (persistencia)",
                    "repo", "normal", False,
                ),
                (
                    "▶  Aplicar Refactorización → Conectar clases",
                    "finish", "success", False,
                ),
            ],
            code_module="ui.code_content_srp",
        )

    def handle_action(self, action: str):
        if action == "break":
            self._simulate_break()
        elif action == "stats":
            self._create_stats()
        elif action == "repo":
            self._create_repo()
        elif action == "finish":
            self._finish_refactor()

    # ── Acciones ──────────────────────────────

    def _simulate_break(self):
        self.state.broken    = True
        self.state.stability = max(0, self.state.stability - 35)
        self.overlay.show(
            kind="danger",
            title="¡SISTEMA INESTABLE!",
            body=[
                "Al intentar actualizar get_full_length() en",
                "la clase Video, accidentalmente rompiste save().",
                "",
                "¿Por qué? Ambas responsabilidades están",
                "ACOPLADAS en la misma clase.",
                "Cambiar una parte afecta a la otra.",
                "",
                "Esto es lo que el SRP busca evitar.",
                "¡Separalas con la herramienta de refactorización!",
            ],
            btn_text="ENTENDIDO — VOY A REFACTORIZAR",
        )
        self.panel.set_tab("broken")

    def _create_stats(self):
        if self.state.stats_created:
            return
        self.state.stats_created   = True
        self.state.step            = STEP_STATS
        self.state.maintainability = min(100, self.state.maintainability + 40)
        self.state.stability       = min(100, self.state.stability + 20)
        self.state.broken          = False
        self.state.add_score(SCORE_STATS)
        self.panel.set_tab("stats")
        self.overlay.show(
            kind="success",
            title="VideoStats CREADA  ✅",
            body=[
                "¡Bien! Extrajiste la lógica de cálculo",
                "a la nueva clase VideoStats.",
                "",
                "Ahora esta clase tiene una sola razón",
                "para cambiar: si la lógica de cálculo",
                "de duración o tamaño necesita actualizarse.",
                "",
                "Siguiente paso: extraé la persistencia",
                "de datos a VideoRepository.",
            ],
            btn_text="CONTINUAR",
        )

    def _create_repo(self):
        if self.state.repo_created or not self.state.stats_created:
            return
        self.state.repo_created    = True
        self.state.step            = STEP_REPO
        self.state.maintainability = min(100, self.state.maintainability + 40)
        self.state.stability       = min(100, self.state.stability + 20)
        self.state.add_score(SCORE_REPO)
        self.panel.set_tab("repo")
        self.overlay.show(
            kind="success",
            title="VideoRepository CREADA  ✅",
            body=[
                "¡Excelente! VideoRepository maneja",
                "toda la persistencia de datos.",
                "",
                "Esta clase solo cambiará si la forma de",
                "guardar en la base de datos cambia.",
                "",
                "Las dos clases son INDEPENDIENTES entre sí.",
                "¡Ahora conectalas para completar el nivel!",
            ],
            btn_text="CONTINUAR",
        )

    def _finish_refactor(self):
        if not (self.state.stats_created and self.state.repo_created):
            return
        self.state.step            = STEP_DONE
        self.state.maintainability = 100
        self.state.stability       = 100
        self.state.add_score(SCORE_FINISH)
        self.win.visible = True
