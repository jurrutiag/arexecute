import json
from executer.executer import Executer
from json_creator.jsonDirections import JsonDirections
from pynput.keyboard import Key, Listener
import pyautogui
import copy

from recorder.recorder import Recorder


class RecorderExecuter:
    _method_translation = {"Mv": "move", "Clk": "click", "Wr": "write", "Var": "variable", "W": "wait"}

    def __init__(self, json_filename, record=False, iterations=1,
                 directory="D:/Docs universidad/My programs/Action_Record_Execute/setup_json_files/", move_duration=1,
                 click_interval=0.1, write_duration=0.1):
        self._move_duration = move_duration
        self._click_interval = click_interval
        self._write_duration = write_duration

        self._json_filename = json_filename
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
        for i in range(self._iterations):
            if self._record:
                self.record()
            else:
                self.execute(i + 1)

    def execute(self, i):
        while self._executer.notEmpty() > 0:
            self._executer.execute(i)

        self._executer.reset()

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

    def getDirections(self):
        return self._directions


# Test functionalities, delete after release
if __name__ == "__main__":
    import time

    # recorder = RecorderExecuter("testNewFile.json", True)
    # recorder.setUp()
    # recorder.start()

    # time.sleep(1)
    # recorder = RecorderExecuter("testNewFile.json", iterations=4)
    # recorder.setUp()
    # recorder.start()
    # print(recorder.getDirections())

    recorder = RecorderExecuter("testDeepEdit.json", iterations=3)
    recorder.setUp()
    recorder.start()

    # time.sleep(1)
    # recorder = RecorderExecuter("testDeepEdit.json", iterations=3)
    # recorder.setUp()
    # recorder.start()
    # print(recorder.getDirections())
