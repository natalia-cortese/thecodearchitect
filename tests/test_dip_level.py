"""
Tests for levels/dip_level.py
"""

import pytest
from core.state import GameState
from core.constants import DIP_STEP_CHAOS, DIP_STEP_ABSTRACT, DIP_STEP_INJECT
from levels.dip_level import DIPLevel


class TestDIPLevel:
    """Test DIP Level logic and state transitions."""

    @pytest.fixture
    def dip_level(self, mock_panel, mock_overlay, mock_win_screen):
        level = DIPLevel()
        state = GameState()
        level.setup(state, mock_panel, mock_overlay, mock_win_screen)
        return level, state, mock_panel, mock_overlay, mock_win_screen

    def test_dip_step_constants(self):
        assert DIP_STEP_CHAOS == 0
        assert DIP_STEP_ABSTRACT == 1
        assert DIP_STEP_INJECT == 2

    def test_level_metadata(self):
        assert DIPLevel.level_number == 5
        assert DIPLevel.principle == "D.I.P."
        assert "DIP" in DIPLevel.subtitle

    def test_initial_setup(self, dip_level):
        level, state, panel, overlay, win = dip_level
        assert state.interface_created is False
        assert state.client_refactored is False
        assert state.broken is False

    def test_create_abstract(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("abstract")
        assert state.interface_created is True
        assert state.step == DIP_STEP_ABSTRACT
        assert state.score == 250

    def test_inject_dependency_requires_abstract(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("inject")
        assert state.client_refactored is False

    def test_inject_dependency_after_abstract(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("abstract")
        level.handle_action("inject")
        assert state.client_refactored is True
        assert state.step == DIP_STEP_INJECT
        assert state.score == 600

    def test_complete_level(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("abstract")
        level.handle_action("inject")
        assert state.maintainability == 100
        assert state.stability == 100
        assert state.score == 600

    def test_simulate_break(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("break")
        assert state.broken is True
        assert state.stability < 100

    def test_score_accumulation(self, dip_level):
        level, state, panel, overlay, win = dip_level
        assert state.score == 0
        level.handle_action("abstract")
        assert state.score == 250
        level.handle_action("inject")
        assert state.score == 600

    def test_no_double_abstract(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("abstract")
        level.handle_action("abstract")
        assert state.score == 250

    def test_no_double_inject(self, dip_level):
        level, state, panel, overlay, win = dip_level
        level.handle_action("abstract")
        level.handle_action("inject")
        level.handle_action("inject")
        assert state.score == 600
