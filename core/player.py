"""
Sistema de jugadores y puntuación.
Compatible con desktop y WebAssembly (Pygbag).
"""

import json
import sys
from pathlib import Path


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
        self._players: dict[str, Player] = {}
        self._current_player: Player | None = None
        self._load_players()

    @classmethod
    def get_instance(cls) -> "PlayerManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_players(self):
        try:
            if sys.platform == "emscripten":
                import js
                data = js.eval("localStorage.getItem('code_architect_players')")
                if data:
                    parsed = json.loads(data)
                    self._players = {
                        name: Player.from_dict(pdata)
                        for name, pdata in parsed.items()
                    }
                    current = js.eval("localStorage.getItem('code_architect_current')")
                    if current and current in self._players:
                        self._current_player = self._players[current]
            else:
                data_dir = Path.home() / ".code_architect"
                data_dir.mkdir(parents=True, exist_ok=True)
                players_file = data_dir / "players.json"
                current_file = data_dir / "current_player.txt"
                
                if players_file.exists():
                    with open(players_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self._players = {
                            name: Player.from_dict(pdata)
                            for name, pdata in data.items()
                        }
                
                if current_file.exists():
                    current = current_file.read_text().strip()
                    if current in self._players:
                        self._current_player = self._players[current]
        except Exception as e:
            print(f"Warning: Could not load players: {e}")
            self._players = {}

    def _save_players(self):
        try:
            if sys.platform == "emscripten":
                import js
                players_json = json.dumps({n: p.to_dict() for n, p in self._players.items()})
                js.eval(f"localStorage.setItem('code_architect_players', '{players_json.replace(chr(39), chr(34))}')")
                if self._current_player:
                    js.eval(f"localStorage.setItem('code_architect_current', \"{self._current_player.name}\")")
            else:
                data_dir = Path.home() / ".code_architect"
                data_dir.mkdir(parents=True, exist_ok=True)
                players_file = data_dir / "players.json"
                current_file = data_dir / "current_player.txt"
                
                with open(players_file, "w", encoding="utf-8") as f:
                    json.dump({n: p.to_dict() for n, p in self._players.items()}, f, indent=2)
                
                if self._current_player:
                    current_file.write_text(self._current_player.name)
        except Exception as e:
            print(f"Warning: Could not save players: {e}")

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
        self._current_player = player
        self._save_players()
        return player

    def login_player(self, name: str) -> Player | None:
        name = name.strip()
        if name in self._players:
            self._current_player = self._players[name]
            self._save_players()
            return self._current_player
        return None

    def get_current_player(self) -> Player | None:
        return self._current_player

    def logout(self):
        self._current_player = None
        self._save_players()

    def update_score(self, level: str, score: int) -> bool:
        player = self.get_current_player()
        if player is None:
            return False
        updated = player.set_score(level, score)
        if updated:
            self._save_players()
        return updated
