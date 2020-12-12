
from ..filehandler import FileHandler
import pyautogui
from pynput.keyboard import Controller
from dataclasses import dataclass
from ..arkey import ARKey


@dataclass
class ExecuterConfig:
    MOVE_DURATION: float = 0.2
    CLICK_INTERVAL: float = 0.1
    WRITE_SPEED: float = 0.1


class Executer:

    def __init__(self, filename, variables=None, verbose=0, config=None):
        self.filename = filename
        self.verbose = verbose

        self.variables = variables

        self.current_position = None
        self.config = config or ExecuterConfig()

        self.actions = FileHandler.load(self.filename)
        self._keyboard = Controller()

    def start(self):
        translations = {v: k for k, v in self.actions.ACTION_TRANSLATION.items()}
        for action in self.actions.get_actions_list():
            self.__getattribute__(translations[action[0]])(action[1])

    def move(self, pos):
        self.current_position = pos
        pyautogui.moveTo(pos[0], pos[1], duration=self.config.MOVE_DURATION)

    def click(self, clicks):
        pos = self.current_position or list(pyautogui.position())
        pyautogui.click(pos[0], pos[1], clicks=clicks, interval=self.config.CLICK_INTERVAL)

    def variable(self, index):
        pyautogui.typewrite(self.variables[index], self.config.WRITE_SPEED)

    def type_input(self, inp):
        inp = [[ARKey(elem) for elem in inp_list] for inp_list in inp]

        for inp_list in inp:
            for elem in inp_list:
                self._keyboard.press(elem.key_for_action())

            for elem in inp_list:
                self._keyboard.release(elem.key_for_action())
