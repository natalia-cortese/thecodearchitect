"""
Pytest configuration and fixtures for The Code Architect tests.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


import pytest


@pytest.fixture
def game_state():
    """Create a fresh GameState instance."""
    from core.state import GameState
    return GameState()


@pytest.fixture
def mock_panel():
    """Mock panel for level testing."""
    class MockPanel:
        def __init__(self):
            self.buttons = []
            self.current_tab = "broken"
            self._code_content = {}

        def configure(self, tabs=None, buttons=None, code_module=None):
            pass

        def set_tab(self, tab_id):
            self.current_tab = tab_id

        def set_code_content(self, content):
            self._code_content = content

    return MockPanel()


@pytest.fixture
def mock_overlay():
    """Mock feedback overlay for level testing."""
    class MockOverlay:
        def __init__(self):
            self.visible = False
            self.kind = None
            self.title = None
            self.body = None

        def show(self, kind, title, body, btn_text):
            self.visible = True
            self.kind = kind
            self.title = title
            self.body = body

        def hide(self):
            self.visible = False

    return MockOverlay()


@pytest.fixture
def mock_win_screen():
    """Mock win screen for level testing."""
    class MockWinScreen:
        def __init__(self):
            self.visible = False

    return MockWinScreen()
