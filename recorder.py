import json
import stack


class RecorderExecuter():

    def __init__(self, json_filename, record=False, directory="D:/Docs universidad/My programs/Action-Record-Execute/setup_json_files/"):
        self._json_filename = json_filename
        self._record = record
        self._dir = directory
        self._directions = None

    def setUp(self):
        if (self._record):
            open(self._dir + self._json_filename, 'w').close()
            with open("json_template.json", 'r') as f:
                json_template = f.read()
            with open(self._dir + self._json_filename, 'w') as f:
                f.write(json_template)
        else:
            with open(self._dir + self._json_filename, 'r') as f:
                self._directions = json.load(f)

    # Direction types:
    #
    # Directions order, representad as DirOrder, a list with elements representing a direction.
    # Move mouse, represented as MouseDirections key, a stack, pairs (posX, posY), direction representation "Mv"
    # Click mouse, represented as MouseClick key, a stack, pairs (posX, posY, numClicks), direction representation "Clk"

    def start(self):
        if (self._record):
            self.record()
        else:
            self.execute()

    def execute(self):
        directionMain = self._directions["DirOrder"]
        if ("Mv" in directionMain):
            mouseDirections = Stack(self._directions["MouseDirections"])
        if ("Clk" in directionMain):
            mouseClicks = Stack(self._directions["MouseClick"])

        while (len(directionMain) > 0):
            direction = directionMain.get()
            if (direction == "Mv"):
                self.executeMove(mouseDirections.get())
            elif (direction == "Clk"):
                self.executeClick(mouseClicks.get())

    def getDirections(self):
        return self._directions


# Test functionalities, delete after release
if __name__ == "__main__":
    recorder = Recorder("testfile.json")

    recorder.setUp()
    print(recorder.getDirections()["hola"])

    recorder = RecorderExecuter("testNewFile.json", True)
    recorder.setUp()
    recorder = RecorderExecuter("testNewFile.json")
    recorder.setUp()
    print(recorder.getDirections())
