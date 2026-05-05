"""
Constantes globales del juego.
"""

# Pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "The Code Architect — Nivel 1: SRP"
FPS = 60

# ──────────────────────────────────────────────
# Paleta cyberpunk (misma que la versión HTML)
# ──────────────────────────────────────────────
C_BG = (5, 10, 15)
C_PANEL = (10, 21, 32)
C_CYAN = (0, 255, 255)
C_ACCENT = (240, 165, 0)
C_DANGER = (255, 34, 85)
C_SUCCESS = (0, 255, 136)
C_DIM = (26, 48, 64)
C_TEXT = (200, 230, 240)
# Texto del panel de código (más brillante para legibilidad en fondo oscuro)
C_CODE_TEXT = (235, 248, 255)
# Números de línea (visibles pero secundarios)
C_LINE_NUM = (90, 140, 170)
C_CODE_BG = (6, 13, 20)
C_PURPLE = (180, 100, 255)
C_YELLOW = (255, 200, 80)
C_ORANGE = (255, 150, 80)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)

# Transparencias útiles (RGBA)
CYAN_DIM = (0, 255, 255, 30)
DANGER_DIM = (255, 34, 85, 30)
SUCCESS_DIM = (0, 255, 136, 30)

# Layout
CITY_WIDTH = 820  # ancho del canvas de ciudad (izquierda)
PANEL_WIDTH = SCREEN_WIDTH - CITY_WIDTH  # panel derecho
HEADER_HEIGHT = 65
CITY_HEIGHT = SCREEN_HEIGHT - HEADER_HEIGHT

# Pasos del juego
STEP_CHAOS = 0  # estado inicial, clase monstruo
STEP_STATS = 1  # VideoStats extraída
STEP_REPO = 2  # VideoRepository extraída
STEP_DONE = 3  # refactorización completa

# Pasos LSP
LSP_STEP_CHAOS    = 0
LSP_STEP_SEPARATE = 1
LSP_STEP_REFACTOR = 2

# Pasos ISP
ISP_STEP_CHAOS    = 0
ISP_STEP_SEPARATE = 1
ISP_STEP_REFACTOR = 2

# Pasos DIP
DIP_STEP_CHAOS   = 0
DIP_STEP_ABSTRACT = 1
DIP_STEP_INJECT  = 2

# Puntuación
SCORE_BREAK = 0
SCORE_STATS = 200
SCORE_REPO = 200
SCORE_FINISH = 300
