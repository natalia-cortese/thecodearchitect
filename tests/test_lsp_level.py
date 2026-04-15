"""
Tests for levels/lsp_level.py
"""

import pytest
from core.state import GameState
from core.constants import LSP_STEP_SEPARATE, LSP_STEP_REFACTOR
from levels.lsp_level import LSPLevel


class TestLSPLevel:
    """Test LSP Level logic and state transitions."""

    @pytest.fixture
    def lsp_level(self, mock_panel, mock_overlay, mock_win_screen):
        level = LSPLevel()
        state = GameState()
        level.setup(state, mock_panel, mock_overlay, mock_win_screen)
        return level, state, mock_panel, mock_overlay, mock_win_screen

    def test_level_metadata(self):
        assert LSPLevel.level_number == 3
        assert LSPLevel.principle == "L.S.P."
        assert "LSP" in LSPLevel.subtitle

    def test_initial_setup(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        assert state.interface_created is False
        assert state.client_refactored is False
        assert state.broken is False

    def test_separate_interface(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        level.handle_action("separate")
        assert state.interface_created is True
        assert state.step == LSP_STEP_SEPARATE
        assert state.score == 250

    def test_refactor_client_requires_interface(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        level.handle_action("refactor")
        assert state.client_refactored is False

    def test_refactor_client_after_interface(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        level.handle_action("separate")
        level.handle_action("refactor")
        assert state.client_refactored is True
        assert state.step == LSP_STEP_REFACTOR
        assert state.score == 600

    def test_complete_level(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        level.handle_action("separate")
        level.handle_action("refactor")
        assert state.maintainability == 100
        assert state.stability == 100
        assert state.score == 600

    def test_simulate_break(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        level.handle_action("break")
        assert state.broken is True
        assert state.stability < 100

    def test_score_accumulation(self, lsp_level):
        level, state, panel, overlay, win = lsp_level
        assert state.score == 0
        level.handle_action("separate")
        assert state.score == 250
        level.handle_action("refactor")
        assert state.score == 600
