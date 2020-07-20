# arexecute
Application to record actions on the computer and then execute them in a controlled way.

# Recording

To record run the following line:

`python -m arexecute example`

In order to create a json file named example with the saved recording.
The instructions for recording are the following:

(->) Denotes press first one key, then the next
| Command                              | Action                                                       |
|--------------------------------------|--------------------------------------------------------------|
| Alt                                  | Stop recording                                               |
| W -> any number -> W                 | Add waiting time of seconds equal to the number              |
| Caps Lock -> any string -> Caps Lock | Writes the string                                            |
| Ctrl                                 | Move mouse to current mouse position                         |
| Shift n times                        | Clicks n times in the last mouse position determined by Ctrl |
| v                                    | Adds a variable to be defined later                          |
<br/>
In this way, one can record mouse movements, clicks, writing variables, etc.

# Executing

To execute, run the following line:

`python -m arexecute example -e`

This will execute the recorded example once. In order to run more than one time, add an integer after de -e flag.
To run it indefinitely use the -r flag. In order for this command to work, a previous recording named example in the same
directory (or in the one defined with the -d flag) must exist.

# Using Variables

When recording, typing 'v' will add a new variable in place. In order to define this variable, you can go to the json file, 'variable' key
and replace the "var_placeholder" strings for the variable itself. In order to use different variables for different iterations, replace
the same strings by lists of variables.
