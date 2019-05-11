import json
from stack.stack import Stack


class JsonDirections:
    def __init__(self, string, translations):
        self._json_template = json.loads(string)
        self._inverted_translations = {v: k for k, v in translations.items()}
        self._stacks = {"directions_order": Stack([])}

        for value in translations.values():
            self._stacks[value] = Stack([])

    def push(self, direction_type, direction):
        self._stacks[direction_type].push(direction)
        self._stacks["directions_order"].push(self._inverted_translations[direction_type])

    def toJson(self):
        for key, stack in self._stacks.items():
            self._json_template[key] = stack.getArray()

        return self._json_template
