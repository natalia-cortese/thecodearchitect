"""
Tests for core/constants.py
"""

import pytest


class TestConstants:
    """Test that all constants are defined and valid."""

    def test_screen_dimensions(self):
        from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        assert SCREEN_WIDTH == 1280
        assert SCREEN_HEIGHT == 720
        assert SCREEN_WIDTH > 0
        assert SCREEN_HEIGHT > 0

    def test_color_palette(self):
        from core.constants import (
            C_BG, C_PANEL, C_CYAN, C_ACCENT, C_DANGER, C_SUCCESS
        )
        for name, color in [
            ("C_BG", C_BG),
            ("C_PANEL", C_PANEL),
            ("C_CYAN", C_CYAN),
            ("C_ACCENT", C_ACCENT),
            ("C_DANGER", C_DANGER),
            ("C_SUCCESS", C_SUCCESS),
        ]:
            assert isinstance(color, tuple), f"{name} should be a tuple"
            assert len(color) in (3, 4), f"{name} should have 3 or 4 components"
            assert all(0 <= c <= 255 for c in color), f"{name} values should be 0-255"

    def test_layout_constants(self):
        from core.constants import CITY_WIDTH, PANEL_WIDTH, HEADER_HEIGHT, CITY_HEIGHT
        assert CITY_WIDTH + PANEL_WIDTH == 1280
        assert HEADER_HEIGHT > 0
        assert CITY_HEIGHT > 0

    def test_step_constants_are_sequential(self):
        from core.constants import STEP_CHAOS, STEP_STATS, STEP_REPO, STEP_DONE
        assert STEP_CHAOS == 0
        assert STEP_STATS == 1
        assert STEP_REPO == 2
        assert STEP_DONE == 3

    def test_lsp_step_constants(self):
        from core.constants import LSP_STEP_CHAOS, LSP_STEP_SEPARATE, LSP_STEP_REFACTOR
        assert LSP_STEP_CHAOS == 0
        assert LSP_STEP_SEPARATE == 1
        assert LSP_STEP_REFACTOR == 2

    def test_score_constants(self):
        from core.constants import SCORE_BREAK, SCORE_STATS, SCORE_REPO, SCORE_FINISH
        assert SCORE_BREAK == 0
        assert SCORE_STATS == 200
        assert SCORE_REPO == 200
        assert SCORE_FINISH == 300
        assert all(s >= 0 for s in [SCORE_BREAK, SCORE_STATS, SCORE_REPO, SCORE_FINISH])
