"""
The Code Architect — Un videojuego didáctico para aprender SOLID
Punto de entrada principal del juego.
"""

import pygame
import sys
from core.game import Game
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
