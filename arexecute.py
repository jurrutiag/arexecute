import sys
from RecorderExecuter import RecorderExecuter
import argparse
import json

INSTRUCTIONS ="""(->) Denotes press first one key, then the next
                  Alt                - Stop recording
         W -> any number -> W        - Add waiting time of seconds equal to the number
Caps Lock -> any string -> Caps Lock - Writes the string
                  Ctrl               - Move mouse to current mouse position
            Shift n times            - Clicks n times in the last mouse position determined by Ctrl
                  v                  - Adds a variable to be defined later
"""

def main():
    parser = argparse.ArgumentParser(description="Record/Execute keyboard and mouse actions.", prog="Recorder/Executer")

    parser.add_argument("filename", action="store", help="Filename to be used for execution/recording (without extension).")
    parser.add_argument("-e", nargs="?", const=1, action="store", dest="execute", type=int, help="Sets the execution mode on with i iterations (defaults to 1 iteration when number not specified).")
    parser.add_argument("-r", action="store_true", dest="recursively", default=False, help="Runs the execution recursively until process killed. No effect on recording.")
    parser.add_argument("-d", action="store", default=".", dest="directory", help="Directory where the file to be used resides (or will be created), defaults to the current directory.")
    parser.add_argument("-a", action="store", default=None, dest="after_script", help="Sets a python script to be executed after the actions (without .py extension).")

    args = parser.parse_args()

    print("\n========================ACTION RECORD EXECUTE========================\n")

    json_filename = args.filename

    execute = args.execute is not None
    iterations = args.execute

    recorder = RecorderExecuter(json_filename, execute=execute, iterations=iterations, after_script=args.after_script, directory=args.directory)

    # Start recording
    msg = f"{INSTRUCTIONS}\nPress enter to start recording... (to leave just write exit and then enter)" if not execute else "Press enter to start executing... (to leave just write exit and then enter)"
    start = input(msg)

    if start == "exit":
        exit("Program stopped by the user.")

    else:
        print("Recording..." if not execute else "Executing...")

    recorder.setUp()
    recorder.start()

    if execute and args.recursively:
        while True:
            recorder.start()

    input("Process finished successfully, press enter to leave...\n")


if __name__ == "__main__":
    main()