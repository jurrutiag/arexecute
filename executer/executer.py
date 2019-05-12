import pyautogui
from stack.stack import Stack
import copy
import time
from keypresswrapper.keypresswrapper import KeyPressWrapper


class Executer:
    def __init__(self, directions, translations):
        directions_order = list(map(lambda x: translations[x], directions["directions_order"]))
        self._directions_dict = {"directions_order": Stack(directions_order)}

        for value in translations.values():
            if value in directions_order:
                self._directions_dict[value] = Stack(directions[value])

        self._directions_dict_fixed = copy.deepcopy(self._directions_dict)
        self._iteration = 0
        self._keyboard = KeyPressWrapper()

    def move(self):
        direction = self._directions_dict["move"].get()
        print(f"move to: ({direction[0]}, {direction[1]})")
        pyautogui.moveTo(direction[0], direction[1], duration=direction[2])

    def click(self):
        direction = self._directions_dict["click"].get()
        print(f"clicked {direction[2]} time(s) on: ({direction[0]}, {direction[1]})")
        pyautogui.click(direction[0], direction[1], clicks=direction[2], interval=direction[3])

    def write(self):
        direction = self._directions_dict["write"].get()

        print(f"wrote ", end="")

        for elem in direction:
            self._keyboard.press_release(list(map(lambda x:KeyPressWrapper.intStrToKeyCode(x), elem)))

            print(f" {KeyPressWrapper.intStrToKeyCode(elem[-1])}", end="")
            time.sleep(0.2)
        print(f"...")

    def variable(self):
        direction = self._directions_dict["variable"].get()

        pyautogui.typewrite(str(direction[self._iteration]), direction[0])

        print(f"variable {direction[self._iteration - 1]} written")

    def execute(self, i):
        self._iteration = i
        getattr(self, self._directions_dict["directions_order"].get())()

    def notEmpty(self):
        return len(self._directions_dict["directions_order"].getArray()) != 0

    def reset(self):
        self._directions_dict = copy.deepcopy(self._directions_dict_fixed)
