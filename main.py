import pygame
import gui
import state
import event_handler
from multiprocessing import Process, Queue


def voice_listener(_event_handler, queue):
    """
    Listening process, put what Pipi hears into
    a queue which is listened by the GUI
    :param _event_handler:
    :param queue:
    :return:
    """
    command = _event_handler.pipi_listen()
    if command:
        queue.put(command)


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_state.set_state("SSH season voice mode")
    game_gui = gui.GUI(game_state)
    game_event_handler = event_handler.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    commandQueue = Queue()
    listeningProcess = Process(target=voice_listener, args=(game_event_handler, commandQueue,))
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        if not len(game_event_handler.queue) == 0:
            val = game_event_handler.queue.pop()
            if val:
                listeningProcess.start()
            else:
                listeningProcess.terminate()
                listeningProcess.join()
                listeningProcess = Process(target=voice_listener, args=(game_event_handler, commandQueue,))
        if not commandQueue.empty():
            game_gui.command_switch(commandQueue.get())
        pygame.display.update()
        FPS_clock.tick(30)
