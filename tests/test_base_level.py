"""
Tests for levels/base_level.py
"""

import pytest
from levels.base_level import BaseLevel


class TestBaseLevel:
    """Test BaseLevel interface."""

    def test_base_level_is_class(self):
        assert issubclass(BaseLevel, object)

    def test_base_level_has_required_attributes(self):
        assert hasattr(BaseLevel, 'level_number')
        assert hasattr(BaseLevel, 'title')
        assert hasattr(BaseLevel, 'subtitle')
        assert hasattr(BaseLevel, 'principle')

    def test_base_level_has_required_methods(self):
        assert hasattr(BaseLevel, 'setup')
        assert hasattr(BaseLevel, 'handle_action')
        assert hasattr(BaseLevel, 'update_panel_buttons')

    def test_methods_are_callable(self):
        assert callable(getattr(BaseLevel, 'setup'))
        assert callable(getattr(BaseLevel, 'handle_action'))
        assert callable(getattr(BaseLevel, 'update_panel_buttons'))
