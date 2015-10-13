import pygame
import gui
import state
import event_handler
from pygame.locals import *
from multiprocessing import Process


def background_process(recording, _game_state, queue):
    event = pygame.event.poll()
    if event == KEYDOWN:
        if event.key == K_SPACE:
            print "handling"
            if _game_state.get_state() == "SSH season voice mode":
                recording = not recording
                queue.put([recording])


def voice_listener(_event_handler):
    print "listening"
    _event_handler.pipi_listen()


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_state.set_state("SSH season voice mode")
    game_gui = gui.GUI(game_state)
    game_event_handler = event_handler.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    listeningProcess = Process(target=voice_listener, args=(game_event_handler,))
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        if not len(game_event_handler.queue) == 0:
            val = game_event_handler.queue.pop()
            if val:
                print "start listening"
                listeningProcess.start()
            else:
                print "terminating"
                listeningProcess.terminate()
                listeningProcess.join()
                listeningProcess = Process(target=voice_listener, args=(game_event_handler,))
        pygame.display.update()
        FPS_clock.tick(30)
