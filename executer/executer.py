import pyautogui
from stack.stack import Stack


class Executer:
    def __init__(self, directions, translations):
        directions_order = list(map(lambda x: translations[x], directions["directions_order"]))
        self._directions_dict = {"directions_order": Stack(directions_order)}

        for value in translations.values():
            if value in directions_order:
                self._directions_dict[value] = Stack(directions[value])

    def move(self):
        direction = self._directions_dict["move"].get()
        print(f"move to: ({direction[0]}, {direction[1]})\n")
        pyautogui.moveTo(direction[0], direction[1], duration=direction[2])

    def click(self):
        direction = self._directions_dict["click"].get()
        print(f"clicked {direction[2]} time(s) on: ({direction[0]}, {direction[1]})\n")
        pyautogui.click(direction[0], direction[1], clicks=direction[2], interval=direction[3])

    def execute(self):
        getattr(self, self._directions_dict["directions_order"].get())()

    def notEmpty(self):
        return len(self._directions_dict["directions_order"].getArray()) != 0
