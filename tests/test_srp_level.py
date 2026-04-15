"""
Tests for levels/srp_level.py
"""

import pytest
from core.state import GameState
from core.constants import STEP_STATS, STEP_REPO, STEP_DONE
from levels.srp_level import SRPLevel


class TestSRPLevel:
    """Test SRP Level logic and state transitions."""

    @pytest.fixture
    def srp_level(self, mock_panel, mock_overlay, mock_win_screen):
        level = SRPLevel()
        state = GameState()
        level.setup(state, mock_panel, mock_overlay, mock_win_screen)
        return level, state, mock_panel, mock_overlay, mock_win_screen

    def test_level_metadata(self):
        assert SRPLevel.level_number == 1
        assert SRPLevel.principle == "S.R.P."
        assert "SRP" in SRPLevel.subtitle

    def test_initial_setup(self, srp_level):
        level, state, panel, overlay, win = srp_level
        assert state.step == 0
        assert state.stats_created is False
        assert state.repo_created is False
        assert state.broken is False

    def test_create_stats(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("stats")
        assert state.stats_created is True
        assert state.step == STEP_STATS
        assert state.broken is False
        assert state.score == 200

    def test_create_repo_requires_stats(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("repo")
        assert state.repo_created is False

    def test_create_repo_after_stats(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("stats")
        level.handle_action("repo")
        assert state.repo_created is True
        assert state.step == STEP_REPO
        assert state.score == 400

    def test_finish_requires_both_created(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("finish")
        assert state.step != STEP_DONE

    def test_finish_refactor(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("stats")
        level.handle_action("repo")
        level.handle_action("finish")
        assert state.step == STEP_DONE
        assert state.maintainability == 100
        assert state.stability == 100
        assert state.score == 700

    def test_simulate_break(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("break")
        assert state.broken is True
        assert state.stability < 100

    def test_stats_increases_maintainability(self, srp_level):
        level, state, panel, overlay, win = srp_level
        level.handle_action("stats")
        assert state.maintainability > 0

    def test_button_update_logic(self, srp_level):
        level, state, panel, overlay, win = srp_level
        
        class MockButton:
            def __init__(self):
                self.enabled = True
        
        panel.buttons = [MockButton() for _ in range(4)]
        level.update_panel_buttons(state)
        
        assert len(panel.buttons) == 4
        for btn in panel.buttons:
            assert hasattr(btn, 'enabled')
