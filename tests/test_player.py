"""
Tests for core/player.py
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch


class TestPlayer:
    """Test Player class."""

    def test_create_player(self):
        from core.player import Player
        p = Player("TestUser")
        assert p.name == "TestUser"
        assert p.scores == {}
        assert p.total_score == 0

    def test_set_score(self):
        from core.player import Player
        p = Player("TestUser")
        updated = p.set_score("srp", 100)
        assert updated is True
        assert p.scores["srp"] == 100

    def test_set_score_higher_wins(self):
        from core.player import Player
        p = Player("TestUser")
        p.set_score("srp", 100)
        updated = p.set_score("srp", 150)
        assert updated is True
        assert p.scores["srp"] == 150

    def test_set_score_lower_ignored(self):
        from core.player import Player
        p = Player("TestUser")
        p.set_score("srp", 150)
        updated = p.set_score("srp", 100)
        assert updated is False
        assert p.scores["srp"] == 150

    def test_get_score(self):
        from core.player import Player
        p = Player("TestUser", {"srp": 200})
        assert p.get_score("srp") == 200
        assert p.get_score("ocp") == 0

    def test_total_score(self):
        from core.player import Player
        p = Player("TestUser", {"srp": 200, "ocp": 150, "lsp": 100})
        assert p.total_score == 450

    def test_to_dict(self):
        from core.player import Player
        p = Player("TestUser", {"srp": 200})
        data = p.to_dict()
        assert data == {"name": "TestUser", "scores": {"srp": 200}}

    def test_from_dict(self):
        from core.player import Player
        data = {"name": "TestUser", "scores": {"srp": 200}}
        p = Player.from_dict(data)
        assert p.name == "TestUser"
        assert p.scores == {"srp": 200}


class TestPlayerManager:
    """Test PlayerManager class with temp directory."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path

    @pytest.fixture
    def manager(self, temp_dir):
        with patch("core.player.DATA_DIR", temp_dir):
            with patch("core.player.PLAYERS_FILE", temp_dir / "players.json"):
                with patch("core.player.CURRENT_FILE", temp_dir / "current.txt"):
                    from core.player import PlayerManager
                    PlayerManager._instance = None
                    m = PlayerManager()
                    yield m
                    PlayerManager._instance = None

    def test_create_player(self, manager):
        player = manager.create_player("Alice")
        assert player.name == "Alice"
        assert manager.get_current_player() == player

    def test_login_existing_player(self, manager):
        manager.create_player("Bob")
        manager.logout()
        player = manager.login_player("Bob")
        assert player is not None
        assert player.name == "Bob"

    def test_login_nonexistent_player(self, manager):
        player = manager.login_player("Nobody")
        assert player is None

    def test_update_score(self, manager):
        manager.create_player("Charlie")
        updated = manager.update_score("srp", 300)
        assert updated is True
        assert manager.get_current_player().scores["srp"] == 300

    def test_update_score_no_player(self, manager):
        updated = manager.update_score("srp", 300)
        assert updated is False

    def test_leaderboard(self, manager):
        p1 = manager.create_player("Player1")
        p1.set_score("srp", 100)
        manager.logout()
        p2 = manager.create_player("Player2")
        p2.set_score("srp", 200)
        manager.logout()

        lb = manager.get_leaderboard()
        assert lb[0].name == "Player2"
        assert lb[1].name == "Player1"
