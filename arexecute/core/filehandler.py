from json.encoder import JSONEncoder
from pathlib import Path
import json
from .actions import Actions
from .arkey import ARKey


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ARKey):
            return obj.toJSON()

        return json.JSONEncoder.default(self, obj)


class JSONHandler:
    EXTENSION = ".json"

    @staticmethod
    def save(recorder, filepath):
        actions_dict = {
            "actions": recorder.actions.get_actions_list(),
            "screen_size": recorder.actions.screen_size
        }

        with open(filepath, 'w') as f:
            json.dump(actions_dict, f, cls=CustomJSONEncoder)

    @staticmethod
    def load(filepath):
        with open(filepath, 'r') as f:
            actions_dict = json.load(f)

        actions = Actions(actions_dict['screen_size'], actions=actions_dict['actions'])
        return actions


class FileHandler:
    HANDLER = JSONHandler

    @staticmethod
    def _preprocess(filename):
        if not str(filename).endswith(FileHandler.HANDLER.EXTENSION):
            filename = str(filename) + FileHandler.HANDLER.EXTENSION

        return Path(str(filename))

    @staticmethod
    def save(recorder):
        filepath = FileHandler._preprocess(recorder.filename)
        FileHandler.HANDLER.save(recorder, filepath)

    @staticmethod
    def load(filename):
        filepath = FileHandler._preprocess(filename)
        return FileHandler.HANDLER.load(filepath)