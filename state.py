import time
import event_handler


class GameState:
    """
    The game state
    """
    def __init__(self):
        self.state = "welcome"

    def reset(self):
        self.result = None
        self.players = []
        self.time_tracker = None
        self.done_creatingTimeTrackers = False
        self.done_settingGameOver = False

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state