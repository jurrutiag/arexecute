import sys
from RecorderExecuter import RecorderExecuter
import argparse
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Record/Execute keyboard and mouse actions.", prog="Recorder/Executer")

    parser.add_argument("filename", action="store", help="Filename to be used for execution/recording (without extension).")
    parser.add_argument("-e", nargs="?", const=1, action="store", dest="execute", type=int, help="Sets the execution mode on with i iterations.")
    parser.add_argument("-r", action="store_true", dest="recursively", default=False, help="Runs the execution recursively. No effect on recording.")
    parser.add_argument("-d", action="store", default=".", dest="directory", help="Directory where the file to be used resides (or will be created).")
    parser.add_argument("-a", action="store", default=None, dest="after_script", help="Sets a script to be executed after the actions.")

    args = parser.parse_args()

    json_filename = args.filename

    execute = args.execute is not None
    iterations = args.execute

    recorder = RecorderExecuter(json_filename, execute=execute, iterations=iterations, after_script=args.after_script, directory=args.directory)

    instructions = "(->) Denotes press first one key, then the next\nAlt - Stop recording\nW -> any number -> W - Add waiting time of number\nCaps Lock -> any string -> Caps Lock - Writes the string\nCtrl - Move mouse to current mouse position\nShift n times - Clicks n times in the last mouse position determined by Ctrl\n"

    # Start recording
    msg = f"{instructions}\nPress enter to start recording... (to leave just write exit and then enter)" if not execute else "Press enter to start executing... (to leave just write exit and then enter)"
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

    if not execute:
        vNum = recorder.variableNumber()
        if vNum > 0:
            vars = []
            for var in range(vNum):
                duration = input(f"Enter the writing duration of the variable {var + 1} (float): \n")

                input_type = input(f"Enter the variable {var + 1} type (str, int, float): \n")
                vi = input(f"Enter varibles array number {var + 1} (for a singleton (1 iteration) [x], for strings use quotes [\"a\", \"b\", ...]): \n")
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

    input("Process finished successfully, press enter to leave...\n")
