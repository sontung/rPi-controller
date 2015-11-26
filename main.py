import pygame
import gui
import state
import event_handler
from multiprocessing import Process, Manager


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
    game_gui = gui.GUI(game_state)
    game_event_handler = event_handler.EventLogic(game_state, game_gui)
    game_gui.add_handler(game_event_handler)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    commandQueue = Manager().Queue()
    listeningProcess = Process(target=voice_listener, args=(game_event_handler, commandQueue,))
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        if game_state.get_state() == "SSH season voice mode" or game_state.get_state() == "Web season voice mode":
            if not game_event_handler.queue.empty():
                val = game_event_handler.queue.get()
                if val:
                    listeningProcess.start()
                else:
                    listeningProcess.terminate()
                    listeningProcess.join()
                    listeningProcess = Process(target=voice_listener, args=(game_event_handler, commandQueue,))
            if not commandQueue.empty():
                voice_command = commandQueue.get()
                try:
                    game_event_handler.pipi.say(voice_command %
                                                game_gui.bool_to_text[str(game_gui.light_to_string[voice_command])])
                except KeyError:
                    pass
        pygame.display.update()
        FPS_clock.tick(30)
