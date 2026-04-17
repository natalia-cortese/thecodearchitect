"""
Sistema de jugadores y puntuación local.
Guarda en un archivo JSON para persistencia.
"""

import json
import os
from pathlib import Path


DATA_DIR = Path.home() / ".code_architect"
PLAYERS_FILE = DATA_DIR / "players.json"
CURRENT_FILE = DATA_DIR / "current_player.txt"


class Player:
    MAX_NAME_LENGTH = 20

    def __init__(self, name: str, scores: dict = None):
        self.name = name
        self.scores = scores or {}

    def set_score(self, level: str, score: int):
        old_score = self.scores.get(level, 0)
        if score > old_score:
            self.scores[level] = score
            return True
        return False

    def get_score(self, level: str) -> int:
        return self.scores.get(level, 0)

    @property
    def total_score(self) -> int:
        return sum(self.scores.values())

    def to_dict(self) -> dict:
        return {"name": self.name, "scores": self.scores}

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(data["name"], data.get("scores", {}))


class PlayerManager:
    _instance = None

    def __init__(self):
        self._ensure_data_dir()
        self._players: dict[str, Player] = {}
        self._current_player: Player | None = None
        self._load_players()

    @classmethod
    def get_instance(cls) -> "PlayerManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _ensure_data_dir(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _load_players(self):
        if PLAYERS_FILE.exists():
            try:
                with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._players = {
                        name: Player.from_dict(pdata)
                        for name, pdata in data.items()
                    }
            except (json.JSONDecodeError, KeyError):
                self._players = {}

    def _save_players(self):
        with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
            data = {name: p.to_dict() for name, p in self._players.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all_players(self) -> list[Player]:
        return list(self._players.values())

    def get_leaderboard(self) -> list[Player]:
        return sorted(self._players.values(), key=lambda p: p.total_score, reverse=True)

    def create_player(self, name: str) -> Player:
        name = name.strip()[: Player.MAX_NAME_LENGTH]
        if not name:
            raise ValueError("El nombre no puede estar vacío")
        if name in self._players:
            player = self._players[name]
        else:
            player = Player(name)
            self._players[name] = player
            self._save_players()
        self._current_player = player
        self._save_current_player()
        return player

    def login_player(self, name: str) -> Player | None:
        name = name.strip()
        if name in self._players:
            self._current_player = self._players[name]
            self._save_current_player()
            return self._current_player
        return None

    def get_current_player(self) -> Player | None:
        if self._current_player is None:
            last_name = self._get_last_player_name()
            if last_name and last_name in self._players:
                self._current_player = self._players[last_name]
        return self._current_player

    def logout(self):
        self._current_player = None
        if CURRENT_FILE.exists():
            CURRENT_FILE.unlink()

    def _get_last_player_name(self) -> str | None:
        if CURRENT_FILE.exists():
            return CURRENT_FILE.read_text().strip()
        return None

    def _save_current_player(self):
        if self._current_player:
            CURRENT_FILE.write_text(self._current_player.name)

    def update_score(self, level: str, score: int) -> bool:
        player = self.get_current_player()
        if player is None:
            return False
        updated = player.set_score(level, score)
        if updated:
            self._save_players()
        return updated
