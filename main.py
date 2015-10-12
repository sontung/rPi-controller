import pygame
import gui
import state
import event_handler
import threading
from multiprocessing import Process, Queue


class MyThread(threading.Thread):
    def __init__(self, name, method_run, optional=None):
        threading.Thread.__init__(self)
        self.name = name
        self.method_run = method_run
        self.optional = optional

    def run(self):
        print self.name
        if self.optional:
            self.method_run(self.optional())
        else:
            self.method_run()


def handler1():
    game_event_handler.event_handler()

def listener1():
    game_event_handler.pipi_listen()


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_state.set_state("SSH season voice mode")
    game_gui = gui.GUI(game_state)
    global game_event_handler
    game_event_handler = event_handler.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_gui.draw(game_state.get_state())
        handler = Process(target=handler1)
        handler.start()
        listener = Process(target=listener1)
        if game_gui.recording:
            listener.start()
        else:
            if listener.is_alive():
                listener.terminate()
                listener.join()
        pygame.display.update()
        FPS_clock.tick(30)
