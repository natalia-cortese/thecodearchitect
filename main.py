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
from core.player import PlayerManager
from ui.menu_screen import MenuScreen


async def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    menu = MenuScreen(screen)
    game = None
    player_manager = PlayerManager.get_instance()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if menu.visible:
                result = menu.handle_event(event)
                if isinstance(result, int):
                    menu.visible = False
                    game = Game(screen, clock, start_level=result + 1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu.visible = True
                    menu._selected_level = None
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.win.visible:
                        action = game.win.handle_click(event.pos)
                        if action == "restart":
                            game._init_level()
                        elif action == "menu":
                            menu.visible = True
                            game = None
                    elif game.overlay.visible:
                        game.overlay.handle_click(event.pos)
                    elif game.panel.handle_click(event.pos) == "finish":
                        level_id = game.level.principle.lower().replace(".", "")
                        player_manager.update_score(level_id, game.state.score)

                elif event.type == pygame.MOUSEMOTION:
                    if not game.overlay.visible and not game.win.visible:
                        game.panel.handle_motion(event.pos)

                elif event.type == pygame.MOUSEWHEEL:
                    if not game.overlay.visible and not game.win.visible:
                        game.panel.handle_wheel(
                            pygame.mouse.get_pos(), event.y
                        )

        screen.fill((5, 10, 15))

        if menu.visible:
            menu.draw()
        elif game:
            dt = clock.tick(FPS) / 1000.0
            game.city.update(dt, game.state)
            game.panel.update(dt)
            game.level.update_panel_buttons(game.state)
            game.overlay.update(dt)

            from core.constants import C_BG, CITY_WIDTH, HEADER_HEIGHT, C_DIM
            screen.fill(C_BG)
            game._draw_grid()
            city_surf = game.city.draw()
            screen.blit(city_surf, (0, HEADER_HEIGHT))
            game.hud.draw(game.state)
            game.panel.draw()
            pygame.draw.line(
                screen, C_DIM, (CITY_WIDTH, HEADER_HEIGHT),
                (CITY_WIDTH, SCREEN_HEIGHT), 1
            )
            if game.overlay.visible:
                game.overlay.draw()
            if game.win.visible:
                game.win.draw(game.state, game.level_index, len(game.LEVELS))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


asyncio.run(main())
