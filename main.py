"""
The Code Architect — Un videojuego didáctico para aprender SOLID
Punto de entrada principal del juego.
Compatible con Pygbag (WebAssembly) y Pygame desktop.
"""

import asyncio
import sys

import pygame

from core.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from core.game import Game


async def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)

    # Loop asíncrono requerido por Pygbag (asyncio.sleep(0) cede el
    # control al browser en cada frame; en desktop no tiene efecto).
    while True:
        alive = game.tick()
        if not alive:
            break
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


asyncio.run(main())
