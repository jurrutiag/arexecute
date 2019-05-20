import pyautogui
from collections import deque
import copy
import time
from keypresswrapper.keypresswrapper import KeyPressWrapper


class Executer:
    def __init__(self, directions, translations):
        directions_order = list(map(lambda x: translations[x], directions["directions_order"]))
        self._directions_dict = {"directions_order": deque(directions_order)}

        for value in translations.values():
            if value in directions_order:
                self._directions_dict[value] = deque(directions[value])

        self._directions_dict_fixed = copy.deepcopy(self._directions_dict)
        self._iteration = 0
        self._keyboard = KeyPressWrapper()

    def move(self):
        direction = self._directions_dict["move"].popleft()
        print(f"moved to: ({direction[0]}, {direction[1]})")
        pyautogui.moveTo(direction[0], direction[1], duration=direction[2])

    def click(self):
        direction = self._directions_dict["click"].popleft()
        print(f"clicked {direction[2]} time(s) on: ({direction[0]}, {direction[1]})")
        pyautogui.click(direction[0], direction[1], clicks=direction[2], interval=direction[3])

    def write(self):
        direction = self._directions_dict["write"].popleft()

        print(f"wrote ", end="")

        for elem in direction:
            self._keyboard.press_release(list(map(lambda x:KeyPressWrapper.intStrToKeyCode(x), elem)))

            print(f" {str(KeyPressWrapper.intStrToKeyCode(elem[-1]))}", end="")
            time.sleep(0.2)
        print(f"...")

    def variable(self):
        direction = self._directions_dict["variable"].popleft()

        pyautogui.typewrite(str(direction[self._iteration]), direction[0])

        print(f"variable {direction[self._iteration]} written")

    def wait(self):
        direction = self._directions_dict["wait"].popleft()

        for i in range(int(direction[0]), -1, -1):
            print(f"waiting for {float(i)} seconds")
            time.sleep(1)

    def execute(self, i):
        self._iteration = i
        getattr(self, self._directions_dict["directions_order"].popleft())()

    def notEmpty(self):
        return len(self._directions_dict["directions_order"]) != 0

    def reset(self):
        self._directions_dict = copy.deepcopy(self._directions_dict_fixed)
