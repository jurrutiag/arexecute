from pynput.keyboard import Key, KeyCode


class ARKey:

    def __init__(self, key):
        self.isctrl = False
        self.ischar = False

        if isinstance(key, (Key, KeyCode)):
            self.isctrl = (key == Key.ctrl_l) or (key == Key.ctrl_r)
            self.key = key

        elif isinstance(key, int):
            try:
                self.key = Key(KeyCode.from_vk(key))

            except ValueError:
                self.key = KeyCode.from_vk(key)

        elif isinstance(key, str):
            self.key = KeyCode.from_char(key)

    def __eq__(self, other):
        return self.key == other.key

    def key_for_action(self):
        return self.key

    def processed(self):
        if isinstance(self.key, KeyCode):
            return self.key.char.lower()

        else:
            return self.key

    def toJSON(self):
        if isinstance(self.key, Key):
            value = self.key.value.vk

        elif isinstance(self.key, KeyCode):
            value = self.key.char

        else:
            value = self.key

        return value

