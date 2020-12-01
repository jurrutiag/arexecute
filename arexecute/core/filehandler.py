from pathlib import Path
import json


class JSONHandler:
    EXTENSION = ".json"

    @staticmethod
    def save(recorder, filepath):
        actions_dict = {
            "actions": recorder.actions.get_actions_list(),
            "screen_size": recorder.screen_size
        }

        with open(filepath, 'w') as f:
            json.dump(actions_dict, f)


class FileHandler:
    HANDLER = JSONHandler

    @staticmethod
    def save(recorder):
        filename = recorder.filename
        if not str(filename).endswith(FileHandler.HANDLER.EXTENSION):
            filename = str(filename) + FileHandler.HANDLER.EXTENSION

        filepath = Path(str(filename))

        FileHandler.HANDLER.save(recorder, filepath)
