import json
from executer.executer import Executer
from json_creator.jsonDirections import JsonDirections
from pynput.keyboard import Key, Listener
import pyautogui


class RecorderExecuter:
    _method_translation = {"Mv": "move", "Clk": "click"}

    def __init__(self, json_filename, record=False,
                 directory="D:/Docs universidad/My programs/Action_Record_Execute/setup_json_files/", move_duration=1,
                 click_interval=0.1):
        self._move_duration = move_duration
        self._click_interval = click_interval
        self._json_filename = json_filename
        self._record = record
        self._dir = directory
        self._directions = None
        self._executer = None

        self._clicking = False
        self._recording = False
        self._current_record = []
        self._unformatted_json_record = None
        self._json_directions_creator = None

    def setUp(self):
        if self._record:
            open(self._dir + self._json_filename, 'w').close()
            with open("json_template.json", 'r') as f:
                json_template = f.read()
                self._json_directions_creator = JsonDirections(json_template, RecorderExecuter._method_translation)
            with open(self._dir + self._json_filename, 'w') as f:
                f.write(json_template)
        else:
            with open(self._dir + self._json_filename, 'r') as f:
                self._directions = json.load(f)

            self._executer = Executer(self._directions, RecorderExecuter._method_translation)

    # Direction types:
    #
    # Directions order, representad as directions, a list with elements representing a direction.
    # Move mouse, represented as move key, a stack, pairs (posX, posY), direction representation "Mv"
    # Click mouse, represented as click key, a stack, pairs (posX, posY, numClicks), direction representation "Clk"

    def start(self):
        if self._record:
            self.record()
        else:
            self.execute()

    def execute(self):
        while self._executer.notEmpty() > 0:
            self._executer.execute()

    def record(self):

        def on_press(key):
            if key == Key.alt_l:
                print("Stopped.")
                with open(self._dir + self._json_filename, 'w') as f:
                    json.dump(self._json_directions_creator.toJson(), f)
                Listener.stop(listener)

        def on_release(key):

            if key == Key.shift_l and self._recording:

                if not self._clicking:
                    self._current_record = list(pyautogui.position())
                    self._current_record += [1, self._click_interval]
                else:
                    self._current_record[2] += 1
                self._clicking = True

            # Recording
            if key == Key.ctrl_l and not self._recording:
                self._recording = True

                print("Started self._recording...")
            # Stopped Recording
            elif key == Key.ctrl_l and self._recording:
                self._recording = False

                if not self._clicking:
                    self._current_record = list(pyautogui.position())
                    self._current_record.append(self._move_duration)

                    self._json_directions_creator.push("move", self._current_record)
                    self._current_record = []
                else:
                    self._json_directions_creator.push("click", self._current_record)
                    self._current_record = []

                self._clicking = False

                print("finished recording...")

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def getDirections(self):
        return self._directions


# Test functionalities, delete after release
if __name__ == "__main__":
    recorder = RecorderExecuter("testNewFile.json", True)
    recorder.setUp()
    recorder.start()
    recorder = RecorderExecuter("testNewFile.json")
    recorder.setUp()
    input("enter to start...")
    recorder.start()
    print(recorder.getDirections())

    #recEx = RecorderExecuter("testExecute.json")
    #recEx.setUp()
    #recEx.start()

