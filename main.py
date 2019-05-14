import sys
from recorderexecuter import RecorderExecuter
import json

def checkArgument(arg):
    return "-" + arg in sys.argv


def getArgument(arg):
    return sys.argv[sys.argv.index("-" + arg) + 1]


if __name__ == "__main__":

    # Pre setup
    recordNew = False

    if checkArgument("f"):
        try:
            json_filename = getArgument("f")
        except IndexError:
            exit("Missing argument, enter filename after the -f command")
    elif checkArgument("r"):
        try:
            json_filename = getArgument("r")
            recordNew = True
        except IndexError:
            exit("Missing argument, enter filename after the -r command")
    else:
        exit("Expected file or record command")

    if not recordNew:
        iterations = input("Enter number of iterations (min: 1, max: minimum number of variables to write): ")
        recorder = RecorderExecuter(json_filename, record=recordNew, iterations=int(iterations))
    else:
        recorder = RecorderExecuter(json_filename, record=recordNew)

    recorder.setUp()

    # Start recording
    msg = "Press enter to start recording... (to leave just write exit and then enter)" if recordNew else "Press enter to start executing... (to leave just write exit and then enter)"
    start = input(msg)

    if start == "exit":
        exit("Program stopped by the user.")

    recorder.start()

    if recordNew:
        vNum = recorder.variableNumber()
        if vNum > 0:
            vars = []
            for var in range(vNum):
                duration = input(f"Enter the writing duration of the variable {var + 1} (float): ")

                input_type = input(f"Enter the variable {var + 1} type (str, int, float): ")
                vi = input(f"Enter varibles array number {var + 1} (for a singleton (1 iteration) [x], for strings use quotes [\"a\", \"b\", ...]): ")
                vi = vi.strip("[").strip("]").split(",")
                vi = [v.strip(" ") for v in vi]
                if input_type == "int":
                    vi = [int(v) for v in vi]
                elif input_type == "float":
                    vi = [float(v) for v in vi]
                else:
                    vi = [v.strip("\"") for v in vi]

                vars.append([duration] + vi)

            recorder.defineVariables(vars)

    input("Process finished successfully, press enter to leave...")
