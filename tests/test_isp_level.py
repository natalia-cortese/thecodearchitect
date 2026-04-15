"""
Tests for levels/isp_level.py
"""

import pytest
from core.state import GameState
from core.constants import ISP_STEP_SEPARATE, ISP_STEP_REFACTOR
from levels.isp_level import ISPLevel, ISP_STEP_CHAOS, ISP_STEP_SEPARATE, ISP_STEP_REFACTOR


class TestISPLevel:
    """Test ISP Level logic and state transitions."""

    @pytest.fixture
    def isp_level(self, mock_panel, mock_overlay, mock_win_screen):
        level = ISPLevel()
        state = GameState()
        level.setup(state, mock_panel, mock_overlay, mock_win_screen)
        return level, state, mock_panel, mock_overlay, mock_win_screen

    def test_isp_step_constants(self):
        assert ISP_STEP_CHAOS == 0
        assert ISP_STEP_SEPARATE == 1
        assert ISP_STEP_REFACTOR == 2

    def test_level_metadata(self):
        assert ISPLevel.level_number == 4
        assert ISPLevel.principle == "I.S.P."
        assert "ISP" in ISPLevel.subtitle

    def test_initial_setup(self, isp_level):
        level, state, panel, overlay, win = isp_level
        assert state.interface_created is False
        assert state.client_refactored is False
        assert state.broken is False

    def test_separate_interfaces(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("separate")
        assert state.interface_created is True
        assert state.step == ISP_STEP_SEPARATE
        assert state.score == 250

    def test_refactor_client_requires_interface(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("refactor")
        assert state.client_refactored is False

    def test_refactor_client_after_separate(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("separate")
        level.handle_action("refactor")
        assert state.client_refactored is True
        assert state.step == ISP_STEP_REFACTOR
        assert state.score == 600

    def test_complete_level(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("separate")
        level.handle_action("refactor")
        assert state.maintainability == 100
        assert state.stability == 100
        assert state.score == 600

    def test_simulate_break(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("break")
        assert state.broken is True
        assert state.stability < 100

    def test_score_accumulation(self, isp_level):
        level, state, panel, overlay, win = isp_level
        assert state.score == 0
        level.handle_action("separate")
        assert state.score == 250
        level.handle_action("refactor")
        assert state.score == 600

    def test_no_double_separate(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("separate")
        level.handle_action("separate")
        assert state.score == 250

    def test_no_double_refactor(self, isp_level):
        level, state, panel, overlay, win = isp_level
        level.handle_action("separate")
        level.handle_action("refactor")
        level.handle_action("refactor")
        assert state.score == 600
