import pygame
import gui
import state
import event_handler


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_state.set_state("SSH season")
    game_gui = gui.GUI(game_state)
    game_event_handler = event_handler.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        pygame.display.update()
        FPS_clock.tick(30)
