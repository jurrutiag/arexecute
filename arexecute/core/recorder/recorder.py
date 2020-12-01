from .state import ActionRecordingState
import pyautogui
from pynput.keyboard import Key, Listener
from dataclasses import dataclass
import json
from ..filehandler import FileHandler
from ..actions import Actions


@dataclass
class RecorderConfig:
    MOVE_KEY: Key = Key.ctrl_l
    CLICK_KEY: Key = Key.shift_l
    RECORD_KEY: Key = "r"
    WAIT_KEY: str = "w"
    VARIABLE_PLACE_KEY: str = "v"
    COMMAND_KEY: str = "c"
    END_ACTION_KEY: Key = Key.caps_lock
    EXIT_KEY: Key = Key.alt_l


class Recorder:

    def __init__(self, filename, verbose=0):
        self.filename = filename
        self.verbose = verbose
        self.actions = Actions()
        self.listener = None

        self.screen_size = pyautogui.size()
        self.config = RecorderConfig()

        self.state = ActionRecordingState(self)

    def set_state(self, state):
        self.state = state

    def print(self, message, verbosity=1):
        if self.verbose == verbosity:
            print(message)

    def _on_press(self, key):
        self.state.key_down(key)

    def _on_release(self, key):
        self.state.key_pressed(key)

    def start(self):
        with Listener(on_press=self._on_press, on_release=self._on_release) as self.listener:
            self.listener.join()

    def exit(self):
        FileHandler.save(self)
        self.listener.stop()

