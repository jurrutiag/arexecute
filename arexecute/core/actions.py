

class Actions:
    ACTION_TRANSLATION = {"move": "M", "click": "C", "write": "W", "variable": "V", "wait": "W", "input": "I", "command": "Cm"}

    def __init__(self):
        self.actions = []
        self.variables_index = 0

    def _add_action(self, action):
        self.actions.append(action)

    def get_actions_list(self):
        return self.actions

    def move(self, x, y):
        action = (Actions.ACTION_TRANSLATION["move"], (x, y))
        self._add_action(action)

    def click(self, clicks):
        action = (Actions.ACTION_TRANSLATION["click"], clicks)
        self._add_action(action)

    def variable(self):
        action = (Actions.ACTION_TRANSLATION["variable"], f"var{self.variables_index}")
        self.variables_index += 1
        self._add_action(action)
        
    def record_input(self, inputs):
        action = (Actions.ACTION_TRANSLATION["input"], inputs)
        self._add_action(action)

    def record_command(self, command):
        action = (Actions.ACTION_TRANSLATION["command"], command)
        self._add_action(action)

    def wait(self, time):
        action = (Actions.ACTION_TRANSLATION["wait"], time)
        self._add_action(action)

