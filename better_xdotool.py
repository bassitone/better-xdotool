#!/usr/bin/python3.5
from subprocess import run,check_output,CalledProcessError,DEVNULL
import os
import sys
import re
from termcolor import colored
# TODO add environment preparation code (export DISPLAY=<IP:DISPLAY>, maybe testing the connection itself)
# TODO add error logging?
def main():
    try:
            # Intro and disclaim.

            # TODO: learn how Rapid7 makes those sick 
            #       Metasploit ASCII banners

            print("Better xDoTool v.1.2.1.  ")
            print((colored("No more confusing syntax!\n", 'green')))
            print("Originally by Charles Herrera (@bassitone)\n")
            print("GPL v3, Code is as-is, etc. etc.")
            print("You should have already identified an accessible"
                  " x11 server somehow.")
            print(colored("########################################"
                          "##############", "red"))
            print(colored("\nOnly use this tool when specifically"
                          " given permission.\n", "yellow",
                          attrs=["bold", "underline"]))
            print(colored("With great power comes great responsibility.\n",                           "white", attrs=["bold","underline"]))
            print(colored("################################################"
                          "######", "red"))

            control = ""
            transmit = "" # What we're ultimately going to send.  
                          # Only set after successful user verification
            check = "" # another loop control variable that we'll use
            window = "" # our window ID.  
                        # We may want to save it across commands.
            success = True # boolean for determining if we've satisfied 
                           # dependencies
            trace = 0
            # Enclose command entry logic in a loop.  
            # We might want to send multiple commands, for example.

            # If we have done this before, ask if we'd like 
            # to use the same window
            # TODO: move window stuff to a separate method for 
            #       purposes of elegance.
            #       Requires making this thing into a class with window as 
            #       a global variable

            while control != "x":
                if len(window) > 0:
                    again = input("Would you like to send to"
                            " the same window"
                            " as your previous command?  Type y or n:\n"
                            "Alternatively, you can enter x to quit"
                            " the program\n")
                    if again[0] == "y":
                        cmd = "key --window " + window + " " + command
                        subprocess.run("xdotool " + cmd, shell = True)
                    elif again[0] == "x":
                        close(again[0])
                else:
                    print("First, we need the ID of the window you will be"
                          " sending commands to.\nThis is probably"
                          " a terminal on the remote system,"
                          " but it can be anything")
                    print(colored("Unfortunately, picking your window ID"
                                  " requires a bit of guesswork -\n"
                                  " I can't do it for you", "yellow"))
                    print("If you don't know your window ID,"
                          " please run xwininfo in another terminal.\n"
                          "Consult its manpage for "
                          "any necessary parameters")

                window = input("What is the ID of the window"
                                " you would like to send commands to?\n"
                                "Either 0x***** form or an integer "
                                "is fine\nOtherwise, enter x to quit\n")
                success = False
                while (not success):
                    try:
                        if window[0] == "x":
                            close(window[0])
                        # Prompt for command to send.
                        print(colored("Now I'll ask for the command "
                                        "you would like to send.\n","white",
                                         attrs=["underline"]))
                        print("Normal syntax is fine --"
                              " we'll handle the conversion.\n")
                        print(colored("If you need a special key "
                                        "(shift, ctrl, alt,"
                                      "etc.), type it as written here.\n\n",
                                      "green"))
                        print(colored("Alternatively, type 'x' to exit "
                                      "the program.\n", "yellow"))
                        print(colored("NOTE: Ctrl+C and similar sequences "
                                        "may not work correctly\n"
                                        "      due to limitations in X11 -"
                                        "BE CAREFUL!", "red"))
                        command = input(colored("What command would "
                                                "you like to send to the "
                                                "remote shell?"
                                                "\n\n", "white",
                                            attrs=["bold", "underline"]))
                        success = True
                        # Trigger the exit method.  We verify it below
                        if command == 'x':
                            close(command)
                    except IndexError:
                        print(colored("Sorry, I need a window ID\n", "red"))
                        window = input("Please enter it either as "
                                        "an integer or in 0x***** form\n\n")
                # ask for confirmation.  Shell safely y"all!
                verify = input("Great, you'd like to send '"
                                + command + "'?  Type y or n,"
                                " or x to exit\n\n")

                # correction loop in case we made an error.

                if verify[0] == "y":
                    cmd = prepare(command)
                    transmission = convert_to_x(cmd)
                    trace = send(window, transmission)
                    if trace == 0:
                        print(colored("Command sent.  Please check "
                                      "for your results or any errors.",
                                      "green"))
                        repeat = input("\n\nWould you like to send another "
                                       "command?  Type y or n\n\n")
                        if repeat[0] =="n":
                            close("x")
                    else:
                        print(colored("Command NOT sent."
                                        "  Please try again.", "red",
                                        attrs=["bold"]))
                elif verify[0] == "x":
                    close(verify[0])
    except KeyboardInterrupt:
        print ("")
        sys.exit(-1)
def convert_to_x(s):

    # Take the input strimg and convert it to "x-speak" 
    # in order to interface with xdotool

    # To Hell with it, use string.replace.
    # It"s not pretty or very pythonic, but should get the job done.
    # We"ll validate later.

    the_string = s.replace(" ", "space").replace("!", "exclam").replace("\"", "quotedbl").replace("#", "numbersign").replace("$", "dollar").replace("%", "percent").replace("&", "ampersand").replace("(", "parenleft").replace(")", "parenright").replace("[", "bracketleft").replace("]", "bracketright").replace("*", "asterisk").replace("\\", "backslash").replace("=", "equal").replace("+", "plus").replace(",", "comma").replace("^", "asciicircum").replace("-", "minus").replace("_", "underscore").replace(".", "period").replace("/", "slash").replace(",", "colon").replace(";", "semicolon").replace("<", "less").replace(">", "greater").replace("?", "question").replace("{", "braceleft").replace("}", "braceright").replace("|", "bar").replace("ctrl", "ctrl").replace("alt", "alt").replace("del", "BackSpace").replace("backspace", "BackSpace").replace("Enter", "KP_Enter").replace("Return", "KP_Enter")

    final_string = the_string.replace("~", " ")
    return final_string

def prepare(command_to_send):

    # This method simply checks the command to be sent in "x-speak", 
    # allowing for syntax correction
    # usually whitespace issues

    cmd = command_to_send

    pattern = re.compile('[a-zA-Z-]')
    enter_pattern = re.compile('\b(enter)\b|\b(return)\b')
    ctrl_pattern = re.compile('\b(ctrl)\b')
    alt_pattern = re.compile('\b(alt)\b')
    del_pattern = re.compile('\b(del)\b|\b(backspace)\b')
    #add whitespace to all the things.  We'll trim in a moment

    output = ""
    lcv = 0
    while(lcv < len(cmd)):
        enter_match = re.search(enter_pattern, cmd)
        ctrl_match = re.search(ctrl_pattern, cmd)
        alt_match = re.search(alt_pattern, cmd)
        del_match = re.search(del_pattern, cmd)
        match = re.search(pattern, cmd)
        to_insert = ""
        if enter_match:
            to_insert = "enter"
            lcv += 5
        elif alt_match:
            to_insert = "alt"
            lcv += 3
        elif ctrl_match:
            to_insert = "ctrl"
            lcv += 4
        elif del_match:
            to_insert = "del"
            lcv += 3
        elif match:
            to_insert = cmd[lcv]
            lcv += 1
        output = output + to_insert + "~"
    my_output = output.strip()
    prepared_output = my_output.replace("e~n~t~e~r~", "Enter").replace("a~l~t~", "alt").replace("c~t~r~l~", "ctrl").replace("d~e~l~", "del")

    return prepared_output

def send(window, command):
    # This method builds and sends the command we want to process 
    # via xdotool

    # First, find out if we have what we need on the system we're running on
    try:
        check_requirements()
    except RuntimeError:
        print(colored("Sorry, I'm missing a dependency.\n"
                      "  Please install it and try again.", "red"))
        sys.exit(1) # Since we're missing a dependency, just exit.
    except ValueError:
        print("Please check the IP:DISPLAY you have entered.\n"
                      "Perhaps you need to call 'export DISPLAY=' "
                      "on your remote machine?\n\n")
    # Then build the shell command
    cmd =  "key --window " + window + " " + command

    #Finally, run it.
    try:
        check_output("xdotool " + cmd, shell = True,
                stderr=DEVNULL)
        return 0
    except CalledProcessError:
        print(colored("Something went wrong.  Please try sending"
                        " your command again."))
        return 1
# Part of error handling/environment prep.  
# Should we try to install xdotool if we don't have it?

def check_requirements():
    # Do we have xdotool installed?
    try:
        run('which xdotool', check=True, shell=True, stdout=DEVNULL)
    except CalledProcessError:
        raise RuntimeError("Sorry, xdotool package not found."
         "  Please install it and run this tool again")

    # Do we have a valid window to send commands to?
    display = input("Almost ready.  Before I send the command, I'd like"
            " to make sure I can reach the remote window.\n\nWhat is its IP"            " address and display number?\n"
            " This would usually look something like 192.168.x.x:0\n\n")
    try:
        check_output("xdpyinfo -display " + display, shell=True,
                stderr=DEVNULL)
    except CalledProcessError:
        trace = 1
        raise ValueError()

def close(signal):
    # We call this code in a few different spots
    # might as well make it a method
    # To be used for clean exits (code 0) - errors should exit themselves
    if signal == 'x':
        check = input(colored("Are you sure you would like to quit?  "
                              "Type y or n\n", "yellow", attrs=["bold"]))
        if check == 'y':
            print(colored("Goodbye.", "green"))
            sys.exit(0) # cleaner than break
main()

# EOF
