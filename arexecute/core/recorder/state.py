from pynput.keyboard import Key, KeyCode
import keyboard
import pyautogui
from ..arkey import ARKey


class RecorderState:
    
    def __init__(self, machine):
        self.machine = machine
        self.ended_action = False

    def key_pressed(self, key):
        processed_key = key.processed()

        if processed_key == self.machine.config.MOVE_KEY:
            self.move_key_pressed()

        elif processed_key == self.machine.config.CLICK_KEY:
            self.clicking_key_pressed()

        elif processed_key == self.machine.config.RECORD_KEY:
            self.input_recording_key_pressed()

        elif processed_key == self.machine.config.WAIT_KEY:
            self.waiting_key_pressed()

        elif processed_key == self.machine.config.VARIABLE_PLACE_KEY:
            self.variable_place_key_pressed()

        elif processed_key == self.machine.config.END_ACTION_KEY:
            self.end_action_key_pressed()

        elif processed_key == self.machine.config.EXIT_KEY:
            self.exit_key_pressed()

        self.any_key_pressed(key)

    def move_key_pressed(self):
        pass

    def clicking_key_pressed(self):
        pass

    def input_recording_key_pressed(self):
        pass

    def waiting_key_pressed(self):
        pass

    def variable_place_key_pressed(self):
        pass

    def end_action_key_pressed(self):
        pass

    def exit_key_pressed(self):
        self.machine.set_state(ExitState(self.machine))

    def any_key_pressed(self, key):
        pass

    def key_down(self, key):
        pass


class ActionRecordingState(RecorderState):

    def __init__(self, *args, ending=False, **kwargs):
        super().__init__(*args, **kwargs)

        if ending:
            if self.machine.config.END_ACTION_KEY == Key.caps_lock:
                self.machine._keyboard.press(Key.caps_lock)
                self.machine._keyboard.release(Key.caps_lock)

        self.machine.print("- Listening for actions -")

    def move_key_pressed(self):
        # Coordinates are on image coordinates.
        x, y = list(pyautogui.position())
        self.machine.actions.move(x, y)
        self.machine.print(f"Moved to {x}, {y}")

    def clicking_key_pressed(self):
        self.machine.set_state(ClickingState(self.machine))

    def input_recording_key_pressed(self):
        self.machine.set_state(InputRecordingState(self.machine))

    def waiting_key_pressed(self):
        self.machine.set_state(WaitingTimeSetState(self.machine))

    def variable_place_key_pressed(self):
        self.machine.actions.variable()
        self.machine.print(f"Variable placed")


class ClickingState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicks = 1
        self.machine.print("- Listening for clicks (1 click total) -")

    def _record_clicks(self):
        self.machine.actions.click(self.clicks)
        self.machine.print(f"{self.clicks} clicks recorded")

    def clicking_key_pressed(self):
        self.clicks += 1
        self.machine.print(f"- Listening for clicks ({self.clicks} clicks total) -")

    def end_action_key_pressed(self):
        self._record_clicks()
        self.machine.set_state(ActionRecordingState(self.machine, ending=True))


class InputRecordingState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = []
        self.current_combination = []
        self.current_pressed = []
        self.machine.print("- Listening for input -")

    def key_down(self, key):
        if key in self.current_pressed or key.processed() == self.machine.config.END_ACTION_KEY:
            return

        if hasattr(key.key, 'char') and any(k.isctrl for k in self.current_pressed):
            key = ARKey(chr(ord(key.key.char) + 64).lower())

        self.current_combination.append(key)
        self.current_pressed.append(key)

    def _record_input(self):
        self.machine.actions.type_input(self.inputs)
        self.machine.print(f"Recorded input")

    def end_action_key_pressed(self):
        self._record_input()
        self.machine.set_state(ActionRecordingState(self.machine, ending=True))

    def any_key_pressed(self, key):
        if key.processed() == self.machine.config.END_ACTION_KEY:
            return

        if hasattr(key.key, 'char') and any(k.isctrl for k in self.current_pressed):
            key = ARKey(chr(ord(key.key.char) + 64).lower())

        if len(self.current_pressed) == 1:
            self.current_pressed = []

        if key in self.current_pressed:
            self.current_pressed.remove(key)

        if len(self.current_pressed) == 0:
            self.inputs.append(self.current_combination)
            self.current_combination = []

    def exit_key_pressed(self):
        pass


class ExitState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine.exit()


class WaitingTimeSetState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = ""
        self.machine.print("- Listening for wait time, can be floating point -")

    def _record_waiting(self):
        self.machine.actions.wait(float(self.time))
        self.machine.print(f"Wait with {self.time} seconds recorded")

    def end_action_key_pressed(self):
        if self.time.count(".") > 1:
            self.machine.print("Invalid time (can't have two dots), returning to action state")

        else:
            self._record_waiting()

        self.machine.set_state(ActionRecordingState(self.machine, ending=True))

    def any_key_pressed(self, key):
        if key.processed() == self.machine.config.END_ACTION_KEY:
            return

        if key.processed() in "0123456789.":
            self.time += key.processed()
