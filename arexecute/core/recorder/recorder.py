from .state import ActionRecordingState
import pyautogui
from pynput.keyboard import Key, Listener, Controller
from dataclasses import dataclass
import json
from ..filehandler import FileHandler
from ..actions import Actions
from ..arkey import ARKey


@dataclass
class RecorderConfig:
    MOVE_KEY: Key = Key.ctrl_l
    CLICK_KEY: Key = Key.shift_l
    RECORD_KEY: Key = "r"
    WAIT_KEY: str = "w"
    VARIABLE_PLACE_KEY: str = "v"
    END_ACTION_KEY: Key = Key.caps_lock
    EXIT_KEY: Key = Key.alt_l


class Recorder:

    def __init__(self, filename, verbose=0, config=None):
        self.filename = filename
        self.verbose = verbose
        self.actions = Actions(pyautogui.size())
        self.listener = None

        self.config = config or RecorderConfig()

        self._keyboard = Controller()
        self.state = ActionRecordingState(self)

        self.caps = 0

    def set_state(self, state):
        self.state = state

    def print(self, message, verbosity=1):
        if self.verbose == verbosity:
            print(message)

    def _on_press(self, key):
        self.state.key_down(ARKey(key))

    def _on_release(self, key):
        self.state.key_pressed(ARKey(key))

    def start(self):
        with Listener(on_press=self._on_press, on_release=self._on_release) as self.listener:
            self.listener.join()

    def exit(self):
        FileHandler.save(self)
        if self.caps % 2 == 1:
            keyboard = Controller()
            keyboard.press(Key.caps_lock)
            keyboard.release(Key.caps_lock)

        self.listener.stop()

