import json
from json_creator.jsonDirections import JsonDirections
from pynput.keyboard import Key, Listener
import pyautogui
import copy
from os import walk, system
import os
from collections import deque
import time
from keypresswrapper.keypresswrapper import KeyPressWrapper
from keyset.keyset import KeySet


class RecorderExecuter:
    method_translation = {"Mv": "move", "Clk": "click", "Wr": "write", "Var": "variable", "W": "wait"}
    save_dir = "arexecute_json_files"
    scripts_dir = "arexecute_after_scripts"

    extension = ".json"

    def __init__(self,
                 json_filename,
                 execute=False,
                 iterations=None,
                 after_script=False,
                 directory=None,
                 move_duration=1,
                 click_interval=0.1,
                 write_duration=0.1):

        self._move_duration = move_duration
        self._click_interval = click_interval
        self._write_duration = write_duration

        self._after_script = after_script

        self._json_filename = json_filename + RecorderExecuter.extension
        self._execute = execute

        self._dir = RecorderExecuter.save_dir if directory is None else directory
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)

        self._directions = None

        self._executer = None
        self._recorder = None

        self._iterations = iterations

        self._unformatted_json_record = None
        self._json_directions_creator = None

    def setUp(self):
        if self._execute:
            with open(os.path.join(self._dir, self._json_filename), 'r') as f:
                self._directions = json.load(f)

            self._executer = Executer(copy.deepcopy(self._directions))

        else:
            self._recorder = Recorder(self._move_duration, self._click_interval, self._write_duration, os.path.join(self._dir, self._json_filename))

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
            scripts = list([filename for _, _, filename in walk(RecorderExecuter.scripts_dir)])
            if any(".".join(self._json_filename.split(".")[:-1]) + ".py" in folder for folder in scripts):
                result = system("python " + RecorderExecuter.scripts_dir + "/" + ".".join(self._json_filename.split(".")[:-1]) + ".py" + f" -i {i}")
                if not result == 0:
                    exit("Error on given script...")

    def record(self):

        def on_press(key):
            if key == Key.alt_l and not self._recorder.isListeningWrite():
                with open(os.path.join(self._dir, self._json_filename), 'w') as f:
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
        with open(os.path.join(self._dir, self._json_filename), 'r') as f:
            jsonRead = json.load(f)
            jsonRead["variable"] = vars
        with open(os.path.join(self._dir, self._json_filename), 'w') as f:
            json.dump(jsonRead, f)

    def getDirections(self):
        return self._directions


class Recorder:
    def __init__(self, move_duration, click_interval, write_duration, record_dir):

        open(record_dir, 'w').close()
        self._json_directions_creator = JsonDirections(RecorderExecuter.method_translation)

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


class Executer:
    def __init__(self, directions):
        directions_order = list(map(lambda x: RecorderExecuter.method_translation[x], directions["directions_order"]))
        self._directions_dict = {"directions_order": deque(directions_order)}

        for value in RecorderExecuter.method_translation.values():
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
            self._keyboard.press_release(list(map(lambda x: KeyPressWrapper.intStrToKeyCode(x), elem)))

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
