import pyautogui
from json_creator.jsonDirections import JsonDirections
import json
from keypresswrapper.keypresswrapper import KeyPressWrapper
from keyset.keyset import KeySet


class Recorder:
    def __init__(self, move_duration, click_interval, write_duration, record_dir, translations):

        open(record_dir, 'w').close()
        with open("json_template.json", 'r') as f:
            json_template = f.read()
            self._json_directions_creator = JsonDirections(json_template, translations)

        self._click_interval = click_interval
        self._move_duration = move_duration
        self._write_duration = write_duration

        self._variables_number = 0

        self._waiting_w = False
        self._waiting_w = False
        self._clicking = False
        self._listening_keys = False
        self._last_key = None
        self._variable_count = 0
        self._current_record = []
        self._longpress = []
        self._keyset = KeySet()

    def out_ctrl(self):
        self.terminate_clicking()

        self._current_record = list(pyautogui.position())
        self._current_record.append(self._move_duration)

        self._json_directions_creator.push("move", self._current_record)

        self._current_record = []

        print("Recorded movement...")

    def out_shift(self):
        if not self._clicking:
            self._current_record = list(pyautogui.position())
            self._current_record += [1, self._click_interval]
        else:
            self._current_record[2] += 1
        self._clicking = True

    def terminate_clicking(self):
        if self._clicking:
            self._clicking = False
            self._json_directions_creator.push("click", self._current_record)

            print(f"Recorded {self._current_record[2]} click(s)")

            self._current_record = []

    def out_caps_lock(self):
        self.terminate_clicking()
        if not self._listening_keys:
            self._listening_keys = True
            self._current_record = []
            print("Listening to keys...")
        else:
            self._json_directions_creator.push("write", self._current_record)
            self._current_record = []
            self._listening_keys = False
            print("Stopped listening to keys.")

    def out_v(self):
        self.terminate_clicking()
        print("variable placed.")
        self._variables_number += 1
        self._current_record = [self._write_duration]
        self._json_directions_creator.push("variable", self._current_record)

    def out_w(self):
        self.terminate_clicking()
        if not self._waiting_w:
            self._waiting_w = True
            self._current_record = []
            print("Write waiting time...")
        else:
            try:
                waiting_time = int("".join(list(map(lambda x: str(x[-1]), self._current_record)))[:-1])
            except ValueError:
                waiting_time = 1
            self._json_directions_creator.push("wait", [waiting_time])
            self._current_record = []
            self._waiting_w = False
            print(f"Saved waiting time ({waiting_time}s).")


    def record_write_hold(self, key):
        if key == self._last_key:
            return
        self._last_key = key

        isAlpha = self._keyset.holdKey(key)
        if isAlpha:
            self._current_record.append(self._keyset.toArray())

    def record_write_release(self, key):
        self._last_key = None
        key_set_array = self._keyset.toArray()
        isAlpha = self._keyset.releaseKey(key)
        if not isAlpha and not self._keyset.isCombination():
            self._current_record.append(key_set_array)
            self._keyset.reset()

    def toJson(self):
        return self._json_directions_creator.toJson()

    def isListeningWrite(self):
        return self._listening_keys

    def isListeningClicks(self):
        return self._clicking

    def isWaitingForWait(self):
        return self._waiting_w

    def variableNumber(self):
        return self._variables_number
