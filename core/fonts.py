"""
Gestión centralizada de fuentes.
Usa fuentes del sistema como fallback si no hay assets externos.
"""

import pygame
from functools import lru_cache

pygame.font.init()

# Fuentes monoespaciadas disponibles en el sistema
_MONO_CANDIDATES   = ["Courier New", "Courier", "DejaVu Sans Mono", "monospace"]
_TITLE_CANDIDATES  = ["Impact", "Arial Black", "DejaVu Sans", "sans-serif"]
# Body: fuentes pensadas para legibilidad en pantalla (Verdana, Segoe UI, etc.)
_BODY_CANDIDATES   = [
    "Verdana",        # diseñada para pantalla, muy legible
    "Segoe UI",       # clara en Windows
    "Tahoma",         # buena legibilidad
    "Helvetica",      # estándar en macOS
    "Arial",
    "DejaVu Sans",
    "sans-serif",
]


def _find_font(candidates: list[str]) -> str:
    available = set(pygame.font.get_fonts())
    for name in candidates:
        normalized = name.lower().replace(" ", "")
        if normalized in available:
            return name
    return None   # fallback a SysFont default


@lru_cache(maxsize=32)
def get_font(size: int, kind: str = "body", bold: bool = False) -> pygame.font.Font:
    """
    kind: 'mono' | 'title' | 'body'
    """
    if kind == "mono":
        name = _find_font(_MONO_CANDIDATES)
    elif kind == "title":
        name = _find_font(_TITLE_CANDIDATES)
    else:
        name = _find_font(_BODY_CANDIDATES)

    if name:
        return pygame.font.SysFont(name, size, bold=bold)
    return pygame.font.SysFont(None, size, bold=bold)
