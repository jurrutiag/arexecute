import sys
from recorderexecuter import RecorderExecuter
import argparse
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Record/Execute keyboard and mouse actions.", prog="Recorder/Executer")

    parser.add_argument("-e", action="store", dest="execute", type=int, help="Sets the execution mode on with i iterations.")
    parser.add_argument("-f", action="store_true", dest="forever", default=False, help="Runs the execution forever. No effect on recording.")
    parser.add_argument("-d", action="store", default="D:/Docs universidad/My programs/Action_Record_Execute/setup_json_files/", dest="directory", help="Directory where the file to be used resides (or will be created).")
    parser.add_argument("-s", action="store_true", default=False, dest="after_script", help="Sets the after script mode on.")
    parser.add_argument("filename", action="store", help="Filename to be used for execution/recording (without extension).")

    args = parser.parse_args()

    json_filename = args.filename

    execute = args.execute is not None
    iterations = args.execute

    recorder = RecorderExecuter(json_filename, execute=execute, iterations=iterations, after_script=args.after_script, directory=args.directory)

    recorder.setUp()

    # Start recording
    msg = "Press enter to start recording... (to leave just write exit and then enter)" if not execute else "Press enter to start executing... (to leave just write exit and then enter)"
    start = input(msg)

    if start == "exit":
        exit("Program stopped by the user.")
    else:
        print("Recording...")

    recorder.start()

    if execute and args.forever:
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
