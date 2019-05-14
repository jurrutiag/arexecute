import json
from executer.executer import Executer
from json_creator.jsonDirections import JsonDirections
from pynput.keyboard import Key, Listener
import pyautogui
import copy
from os import walk, system

from recorder.recorder import Recorder


class RecorderExecuter:
    _method_translation = {"Mv": "move", "Clk": "click", "Wr": "write", "Var": "variable", "W": "wait"}
    _scripts_dir = "after_scripts"

    def __init__(self, json_filename, record=False, iterations=None, after_script=False,
                 directory="D:/Docs universidad/My programs/Action_Record_Execute/setup_json_files/", move_duration=1,
                 click_interval=0.1, write_duration=0.1):
        self._move_duration = move_duration
        self._click_interval = click_interval
        self._write_duration = write_duration

        self._after_script = after_script

        self._json_filename = json_filename + ".json"
        self._record = record
        self._dir = directory
        self._directions = None

        self._executer = None
        self._recorder = None

        self._iterations = iterations

        self._unformatted_json_record = None
        self._json_directions_creator = None

    def setUp(self):
        if self._record:
            self._recorder = Recorder(self._move_duration, self._click_interval, self._write_duration,
                                      self._dir + self._json_filename,
                                      RecorderExecuter._method_translation)
        else:
            with open(self._dir + self._json_filename, 'r') as f:
                self._directions = json.load(f)

            self._executer = Executer(copy.deepcopy(self._directions), RecorderExecuter._method_translation)

    # Direction types:
    #
    # Directions order, represented as directions, a list with elements representing a direction.
    # Move mouse, represented as move key, a stack, pairs (posX, posY), direction representation "Mv"
    # Click mouse, represented as click key, a stack, pairs (posX, posY, numClicks), direction representation "Clk"

    def start(self):
        if self._record:
            self.record()
        else:
            for i in range(self._iterations):
                self.execute(i + 1)

    def execute(self, i):
        while self._executer.notEmpty() > 0:
            self._executer.execute(i)

        self.executeScript(i)
        self._executer.reset()

    def executeScript(self, i):
        if self._after_script:
            scripts = list([filename for _, _, filename in walk(RecorderExecuter._scripts_dir)])
            if any(".".join(self._json_filename.split(".")[:-1]) + ".py" in folder for folder in scripts):
                result = system("python " + RecorderExecuter._scripts_dir + "/" + ".".join(self._json_filename.split(".")[:-1]) + ".py" + f" -i {i}")
                if not result == 0:
                    exit("Error on given script...")


    def record(self):

        def on_press(key):
            if key == Key.alt_l and not self._recorder.isListening():
                with open(self._dir + self._json_filename, 'w') as f:
                    json.dump(self._recorder.toJson(), f)
                listener.stop()

            elif (self._recorder.isListening() or self._recorder.isWaitingForWait()) and not key == Key.caps_lock:
                self._recorder.record_write_hold(key)

        def on_release(key):

            if key == Key.ctrl_l and not self._recorder.isListening() and not self._recorder.isWaitingForWait():
                self._recorder.out_ctrl()
            elif key == Key.caps_lock and not self._recorder.isRecording() and not self._recorder.isWaitingForWait():
                self._recorder.out_caps_lock()
            elif key == Key.shift_l and not self._recorder.isListening() and not self._recorder.isWaitingForWait():
                self._recorder.out_shift()
            elif str(
                    key) == "'v'" and not self._recorder.isListening() and not self._recorder.isRecording() and not self._recorder.isWaitingForWait():
                self._recorder.out_v()
            elif str(key) == "'w'" and not self._recorder.isListening() and not self._recorder.isRecording():
                self._recorder.out_w()
            elif (self._recorder.isListening() or self._recorder.isWaitingForWait()) and not key == Key.caps_lock:
                self._recorder.record_write_release(key)

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def variableNumber(self):
        return self._recorder.variableNumber()

    def defineVariables(self, vars):
        with open(self._dir + self._json_filename, 'r') as f:
            jsonRead = json.load(f)
            jsonRead["variable"] = vars
        with open(self._dir + self._json_filename, 'w') as f:
            json.dump(jsonRead, f)

    def getDirections(self):
        return self._directions


if __name__ == "__main__":
    recorder = RecorderExecuter("deepEdit", after_script=True)
    recorder.executeScript(2)
    