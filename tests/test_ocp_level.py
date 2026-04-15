"""
Tests for levels/ocp_level.py
"""

import pytest
from core.state import GameState
from levels.ocp_level import OCPLevel, OCP_STEP_CHAOS, OCP_STEP_INTERFACE, OCP_STEP_REFACTOR, OCP_STEP_EXTEND


class TestOCPLevel:
    """Test OCP Level logic and state transitions."""

    @pytest.fixture
    def ocp_level(self, mock_panel, mock_overlay, mock_win_screen):
        level = OCPLevel()
        state = GameState()
        level.setup(state, mock_panel, mock_overlay, mock_win_screen)
        return level, state, mock_panel, mock_overlay, mock_win_screen

    def test_ocp_step_constants(self):
        assert OCP_STEP_CHAOS == 0
        assert OCP_STEP_INTERFACE == 1
        assert OCP_STEP_REFACTOR == 2
        assert OCP_STEP_EXTEND == 3

    def test_level_metadata(self):
        assert OCPLevel.level_number == 2
        assert OCPLevel.principle == "O.C.P."
        assert "OCP" in OCPLevel.subtitle

    def test_initial_setup(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        assert state.interface_created is False
        assert state.calculator_clean is False
        assert state.extension_added is False

    def test_create_interface(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("interface")
        assert state.interface_created is True
        assert state.step == OCP_STEP_INTERFACE
        assert state.score == 200

    def test_clean_calculator_requires_interface(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("refactor")
        assert state.calculator_clean is False

    def test_clean_calculator_after_interface(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("interface")
        level.handle_action("refactor")
        assert state.calculator_clean is True
        assert state.step == OCP_STEP_REFACTOR
        assert state.score == 400

    def test_extend_requires_calculator_clean(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("extend")
        assert state.extension_added is False

    def test_extend_after_refactor(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("interface")
        level.handle_action("refactor")
        level.handle_action("extend")
        assert state.extension_added is True
        assert state.step == OCP_STEP_EXTEND
        assert state.maintainability == 100
        assert state.stability == 100
        assert state.score == 700

    def test_simulate_break(self, ocp_level):
        level, state, panel, overlay, win = ocp_level
        level.handle_action("break")
        assert state.broken is True
        assert state.stability < 100
