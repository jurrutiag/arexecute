import sys
from recorder import RecorderExecuter


def checkArgument(arg):
    return arg in sys.argv


def getArgument(arg):
    return sys.argv[sys.argv[arg].index() + 1]


if __name__ == "__main__":

    # Pre setup
    recordNew = False

    if checkArgument("f"):
        json_filename = getArgument(f)
    elif checkArgument("r"):
        json_filename = getArgument(r)
        recordNew = True
    else:
        exit("Expected file or record command.")

    recorder = RecorderExecuter(json_filename, record=recordNew)
    recorder.setUp()

    # Start recording
    start = input("Press enter to start recording... (to leave just write exit and then enter)")

    if start == "exit":
        exit("Program stopped by the user.")

    recorder.start()

    input("Process finished successfully, press enter to leave...")
