"""
Tests for core/state.py
"""

import pytest
from core.state import GameState
from core.constants import STEP_CHAOS, STEP_STATS, STEP_DONE


class TestGameState:
    """Test GameState class behavior."""

    def test_initial_state(self, game_state):
        assert game_state.step == STEP_CHAOS
        assert game_state.score == 0
        assert game_state.maintainability == 0
        assert game_state.stability == 100
        assert game_state.stats_created is False
        assert game_state.repo_created is False
        assert game_state.broken is False

    def test_add_score(self, game_state):
        game_state.add_score(100)
        assert game_state.score == 100
        game_state.add_score(200)
        assert game_state.score == 300

    def test_progress_pct_initial(self, game_state):
        assert game_state.progress_pct == 0.0

    def test_progress_pct_at_done(self, game_state):
        game_state.step = STEP_DONE
        assert game_state.progress_pct == pytest.approx(1.0)

    def test_progress_pct_halfway(self, game_state):
        game_state.step = STEP_STATS
        expected = STEP_STATS / 3.0
        assert game_state.progress_pct == pytest.approx(expected)

    def test_broken_flag(self, game_state):
        assert game_state.broken is False
        game_state.broken = True
        assert game_state.broken is True

    def test_stats_created_flag(self, game_state):
        assert game_state.stats_created is False
        game_state.stats_created = True
        assert game_state.stats_created is True
