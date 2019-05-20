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
    _extension = ".json"

    def __init__(self, json_filename, execute=False, iterations=None, after_script=False,
                 directory="D:/Docs universidad/My programs/Action_Record_Execute/setup_json_files/", move_duration=1,
                 click_interval=0.1, write_duration=0.1):
        self._move_duration = move_duration
        self._click_interval = click_interval
        self._write_duration = write_duration

        self._after_script = after_script

        self._json_filename = json_filename + RecorderExecuter._extension
        self._execute = execute
        self._dir = directory
        self._directions = None

        self._executer = None
        self._recorder = None

        self._iterations = iterations

        self._unformatted_json_record = None
        self._json_directions_creator = None

    def setUp(self):
        if self._execute:
            with open(self._dir + self._json_filename, 'r') as f:
                self._directions = json.load(f)

            self._executer = Executer(copy.deepcopy(self._directions), RecorderExecuter._method_translation)
        else:
            self._recorder = Recorder(self._move_duration, self._click_interval, self._write_duration,
                                      self._dir + self._json_filename,
                                      RecorderExecuter._method_translation)

    # Direction types:
    #
    # Directions order, represented as directions, a list with elements representing a direction.
    # Move mouse, represented as move key, a stack, pairs (posX, posY), direction representation "Mv"
    # Click mouse, represented as click key, a stack, pairs (posX, posY, numClicks), direction representation "Clk"

    def start(self):
        if self._execute:
            for i in range(self._iterations):
                self.execute(i + 1)
        else:
            self.record()

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
            if key == Key.alt_l and not self._recorder.isListeningWrite():
                with open(self._dir + self._json_filename, 'w') as f:
                    json.dump(self._recorder.toJson(), f)
                listener.stop()

            elif (self._recorder.isListeningWrite() or self._recorder.isWaitingForWait()) and not key == Key.caps_lock:
                self._recorder.record_write_hold(key)

        def on_release(key):

            if self.isMovementRecordKey(key) and self.canRecordMovement():
                self._recorder.out_ctrl()
            elif self.isWritingRecordKey(key) and self.canWrite():
                self._recorder.out_caps_lock()
            elif self.isClickRecordKey(key) and self.canClick():
                self._recorder.out_shift()
            elif self.isVariablePlaceKey(key) and self.canPlaceVariable():
                self._recorder.out_v()
            elif self.isWaitingPlaceKey(key) and self.canStartWaiting():
                self._recorder.out_w()
            elif (self._recorder.isListeningWrite() or self._recorder.isWaitingForWait()) and not key == Key.caps_lock:
                self._recorder.record_write_release(key)

        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def isMovementRecordKey(self, key):
        return key == Key.ctrl_l

    def canRecordMovement(self):
        return not self._recorder.isWaitingForWait() and not self._recorder.isListeningWrite()

    def isWritingRecordKey(self, key):
        return key == Key.caps_lock

    def canWrite(self):
        return not self._recorder.isWaitingForWait()

    def isClickRecordKey(self, key):
        return key == Key.shift_l

    def canClick(self):
        return not self._recorder.isListeningWrite() and not self._recorder.isWaitingForWait()
    
    def isVariablePlaceKey(self, key):
        return str(key) == "'v'"

    def canPlaceVariable(self):
        return not self._recorder.isListeningWrite() and not self._recorder.isWaitingForWait()

    def isWaitingPlaceKey(self, key):
        return str(key) == "'w'"

    def canStartWaiting(self):
        return not self._recorder.isListeningWrite()

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