from pynput.keyboard import Key
import pyautogui


class RecorderState:
    
    def __init__(self, machine):
        self.machine = machine

    def _filter(self, key):
        try:
            return key.char.lower()

        except AttributeError:
            return key

    def key_pressed(self, key):
        key = self._filter(key)

        if key == self.machine.config.MOVE_KEY:
            self.move_key_pressed()

        elif key == self.machine.config.CLICK_KEY:
            self.clicking_key_pressed()

        elif key == self.machine.config.RECORD_KEY:
            self.input_recording_key_pressed()

        elif key == self.machine.config.WAIT_KEY:
            self.waiting_key_pressed()

        elif key == self.machine.config.VARIABLE_PLACE_KEY:
            self.variable_place_key_pressed()

        elif key == self.machine.config.COMMAND_KEY:
            self.command_key_pressed()

        elif key == self.machine.config.END_ACTION_KEY:
            self.end_action_key_pressed()

        elif key == self.machine.config.EXIT_KEY:
            self.exit_key_pressed()

        else:
            self.other_key_pressed(key)

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

    def command_key_pressed(self):
        pass

    def end_action_key_pressed(self):
        pass

    def exit_key_pressed(self):
        self.machine.set_state(ExitState(self.machine))

    def other_key_pressed(self, key):
        pass

    def key_down(self, key):
        pass


class ActionRecordingState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def command_key_pressed(self):
        self.machine.set_state(CommandRecordingState(self.machine))


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
        self.machine.set_state(ActionRecordingState(self.machine))


class CommandRecordingState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = []
        self.machine.print("- Listening for commands -")

    def _record_command(self):
        self.machine.actions.record_command(self.command)
        self.machine.print(f"Recorded command {' + '.join([str(key) for key in self.command])}")

    def key_down(self, key):
        key = self._filter(key)
        if key in self.command or key == self.machine.config.END_ACTION_KEY:
            return

        self.command.append(key)

    def end_action_key_pressed(self):
        self._record_command()
        self.machine.set_state(ActionRecordingState(self.machine))


class InputRecordingState(RecorderState):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = []
        self.machine.print("- Listening for input (single strokes, not combined comands) -")

    def _record_input(self):
        self.machine.actions.record_input(self.inputs)
        self.machine.print(f"Recorded input")

    def end_action_key_pressed(self):
        self._record_input()
        self.machine.set_state(ActionRecordingState(self.machine))

    def other_key_pressed(self, key):
        self.inputs.append(key)


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
        self._record_waiting()
        self.machine.set_state(ActionRecordingState(self.machine))

    def other_key_pressed(self, key):
        if key in "0123456789.":
            self.time += key
