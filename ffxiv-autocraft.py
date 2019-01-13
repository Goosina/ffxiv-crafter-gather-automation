#!/usr/bin/python3
"""
Use the example to calculate sleep time:
YOUR_MACRO_WAIT_TOTAL + 5

You can manually edit the timers and keystrokes
in the .json file
"""
import json
import os
import sys
import psutil
import re
import time
from pywinauto.application import Application
from pywinauto.keyboard import *

#############
### Intro ###
#############
current_path = os.path.dirname(os.path.abspath(__file__))
# Opening json data file to read
with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
    json_data = json.load(time_data)
# Displaying current macro timers
m_list = [json_data["m1"], json_data["m2"], json_data["m3"], json_data["m4"]]
print("The current macro timers are:\n")
print("m1\tm2\tm3\tm4")
print(*m_list, sep='\t')
# Displaying current keystrokes
k_list = [json_data["k1"], json_data["k2"], json_data["k3"], json_data["k4"]]
print("\nThe current keystrokes are:\n")
print("k1\tk2\tk3\tk4")
print(*k_list, sep='\t')

# argc, argv
argv = sys.argv[1:]
argc = len(argv)

# argument checker
acceptedArguments = ["edit", "editkeys", "autobuff"]
if argc > 1:
    print("  <Error: Too many arguments (must be one).>")
    sys.exit()

if argc == 1 and sys.argv[1] not in acceptedArguments:
    print("  <Error: %s command not found.>" % sys.argv[1])

editor = ""
editedTimerCount = 0
editedKeyCount = 0
try:
    # EDITING MACRO TIMERS
    if sys.argv[1] == "edit":
        editor = "y"
        while editor == "y":
            print("\nFormat example: m1 35")
            print("Which macro timer do you want to edit?")
            # User input
            editThis = input()
            print()

            try:
                if editThis == "":
                    print("  <Error: input cannot be none, try again.>")
                    sys.exit()
                if editThis[2] != ' ':
                    print("Wrong format.\nFormat example: m1 35")
                    sys.exit()
                if len(editThis) < 3:
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
            except IndexError:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()
            # Splitting input into macro and macro timer
            try:
                mtime = int(editThis[3:])
                m = editThis[:2]
            except:
                print("Wrong format.\nFormat example: m1 35")
                sys.exit()

            if m[0] != 'm':
                print("Wrong format.\nFormat example: m1 35")
                sys.exit()
            if mtime < 0 or mtime > 300:
                print("Wrong format.\nFormat example: m1 35\nTime limit is 300")
                sys.exit()

            # Temp adding to json
            with open("%s/ffxiv-autocraft_data.json" % current_path) as add_time_data:
                add_time = json.load(add_time_data)

            print("  ... editing requested macro timer.")
            add_time[m] = mtime

            # Saving to json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "w") as save_time_data:
                json.dump(add_time, save_time_data)
            # Rereading json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
                json_data = json.load(time_data)
                print("  ... saving data...rereading data...done.")

            # Increment times edited
            editedTimerCount += 1

            # Continue or exit
            print("\nDo you want to edit another macro timer? (y/n)")
            editor = input()
            print()
            if editor == "y":
                pass
            elif editor == "n":
                print("  ... Program will continue to auto craft")
                break
            else:
                print(" <Error: input needs to be 'y' or 'n', exiting program.>")
                sys.exit()
    # EDITING KEYS
    if sys.argv[1] == "editkeys":
        editor = "y"
        while editor == "y":
            acceptedKeys = ["1", "2", "3", "4", "5", "6", "7",
                            "8", "9", "0", "-", "="]
            acceptedPlace = ["k1", "k2", "k3", "k4", "k5"]

            print("\nAccepted key edits are the following:\n")
            print(' '.join(map(str, acceptedKeys)))
            print("\nFormat example: k1 3")
            print("Which keystroke do you want to edit?")
            # User input
            editThis = input()
            print()

            try:
                if editThis == "":
                    print("  <Error: input cannot be none, try again.>")
                    sys.exit()
                if editThis[2] != ' ':
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
                if len(editThis) < 3:
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
            except IndexError:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()

            # Splitting input into keys and keystrokes
            try:
                kstroke = str(editThis[3:])
                k = str(editThis[:2])
            except:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()

            if k not in acceptedPlace:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()
            if kstroke not in acceptedKeys:
                print("Keystroke not accepted, check accepted key edits above.")
                sys.exit()

            # Temp adding to json
            with open("%s/ffxiv-autocraft_data.json" % current_path) as add_key_data:
                add_key = json.load(add_key_data)

            print("  ... editing requested keystrokes.")
            add_key[k] = kstroke

            # Saving to json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "w") as save_key_data:
                json.dump(add_key, save_key_data)
            # Rereading json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
                json_data = json.load(time_data)
                print("  ... saving data...rereading data...done.")

            # Increment times edited
            editedKeyCount += 1

            # Continue or exit
            print("\nDo you want to edit another keystroke? (y/n)")
            editor = input()
            print()
            if editor == "y":
                pass
            elif editor == "n":
                print("  ... Program will continue to auto craft")
                break
            else:
                print(" <Error: input needs to be 'y' or 'n', exiting program.>")
                sys.exit()
    # FOOD POT OPTION
    if sys.argv[1] == "autobuff":
        editor = "y"
        while editor == "y":
            # Food/pot tracking variables
            print("Enter your current food buff timer in minutes:")
            foodBuff = input()
            while not isinstance(foodBuff, int):
                try:
                    foodBuff = int(foodBuff)
                except ValueError:
                    print("Food buff timer must be an integer. Please try again:")
                    foodBuff = input()

            while not 3 <= foodBuff <= 60:
                print("Food buff timer needs to be an integer between 3 to 60. Please try again:")
                foodBuff = input()
                foodBuff = int(foodBuff)

            print("Enter your current pot timer in minutes:")
            potBuff = input()
            while not isinstance(potBuff, int):
                try:
                    potBuff = int(potBuff)
                except ValueError:
                    print("Pot buff timer must be an integer. Please try again:")
                    foodBuff = input()
            while not 3 <= foodBuff <= 15:
                print("Pot buff timer needs to be between 3 to 15. Please try again:")
                foodBuff = input()

            foodBuffSeconds = (foodBuff * 60) - 40
            potBuffSeconds = (potBuff * 60) - 40

            # Task Manager -> Right click FFXIV -> Go to details
            process_name = "ffxiv_dx11.exe"

            # AUTO PID
            for proc in psutil.process_iter():
                if proc.name() == process_name:
                    findingPID = re.search('pid=(.+?), name=', str(proc))
                    ffxiv_pid = int(findingPID.group(1))

            # If auto PID doesnt work, check if the 'process_name' is correct in your task manager`
            try:
                app = Application().connect(process=ffxiv_pid)
            except NameError:
                print("  <Error: Process not found.>\n  ... Either make sure FFXIV is running or change 'process_name'")
                sys.exit()

            # Setup sleep times accordingly, and your keystrokes
            print('\nPress Ctrl-C to quit crafting.')
            try:
                food_loss = 0
                pot_loss = 0
                while True:
                    time.sleep(3)
                    food_loss += 3
                    pot_loss += 3
                    if pot_loss >= foodBuffSeconds:
                        time.sleep(1)
                        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_ESCAPE}')
                        print("  ... STANDING UP BY EXITING")
                        time.sleep(4)
                        # POT KEY
                        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k3"])
                        print("  ... EATING FOOD")
                        time.sleep(2)
                        # CRAFT ITEM BUTTON
                        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k5"])
                        print("  ... SELECTING CRAFT")
                        time.sleep(3)
                        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                        print("  ... HIGHLIGHT SELECT CRAFT")
                        time.sleep(2)
                        pot_loss = 0
                        # default 15 min pot buff minus 30 seconds
                        foodBuffSeconds = 870
                    if food_loss >= foodBuffSeconds:
                        time.sleep(1)
                        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_ESCAPE}')
                        print("  ... STANDING UP BY EXITING")
                        time.sleep(4)
                        # FOOD KEY
                        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k4"])
                        print("  ... EATING FOOD")
                        time.sleep(2)
                        # CRAFT ITEM BUTTON
                        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k5"])
                        print("  ... SELECTING CRAFT")
                        time.sleep(3)
                        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                        print("  ... HIGHLIGHT SELECT CRAFT")
                        time.sleep(2)
                        pot_loss = 0
                        # default 30 min pot buff minus 30 seconds
                        foodBuffSeconds = 1770
                    # SELECT "SYNTHESIZE"
                    app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                    print("  ... Selecting the button 'Synthesize'.")
                    time.sleep(3)
                    food_loss += 3
                    pot_loss += 3
                    # PRESS "SYNTHESIZE"
                    app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                    print("  ... Pressing the button 'Synthesize'.")
                    time.sleep(3)
                    food_loss += 3
                    pot_loss += 3
                    # CRAFTING MACRO 1
                    app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k1"])
                    print("  ... Pressing macro 1 ... <wait.{:d}>.".format(json_data["m1"]))
                    time.sleep(json_data["m1"])
                    food_loss += json_data["m1"]
                    pot_loss += json_data["m1"]
                    # CRAFTING MACRO 2
                    app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k2"])
                    print("  ... Pressing macro 2 ... <wait.{:d}>.".format(json_data["m2"]))
                    time.sleep(json_data["m2"])
                    food_loss += json_data["m2"]
                    pot_loss += json_data["m2"]
            except KeyboardInterrupt:
                print("Program has stopped.")
                sys.exit()
except IndexError:
    pass

# Displaying new timers if edited
if editedTimerCount > 0:
    m_list = [json_data["m1"], json_data["m2"], json_data["m3"], json_data["m4"]]
    print("\nThe new macro timers are:\n")
    print("m1\tm2\tm3\tm4")
    print(*m_list, sep='\t')

# Displaying new timers if edited
if editedKeyCount > 0:
    k_list = [json_data["k1"], json_data["k2"], json_data["k3"], json_data["k4"]]
    print("\nThe new keystrokes are:\n")
    print("k1\tk2\tk3\tk4")
    print(*k_list, sep='\t')

# Task Manager -> Right click FFXIV -> Go to details
process_name = "ffxiv_dx11.exe"

# AUTO PID
for proc in psutil.process_iter():
    if proc.name() == process_name:
        findingPID = re.search('pid=(.+?), name=', str(proc))
        ffxiv_pid = int(findingPID.group(1))
        

# If auto PID doesnt work, check if the 'process_name' is correct in your task manager`
try:
    app = Application().connect(process=ffxiv_pid)
except NameError:
    print("  <Error: Process not found.>\n  ... Either make sure FFXIV is running or change 'process_name'")
    sys.exit()

# Setup sleep times accordingly, and your keystrokes
print('\nPress Ctrl-C to quit crafting.')
try:
    while True:
        time.sleep(3)
        # SELECT "SYNTHESIZE"
        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
        print("  ... Selecting the button 'Synthesize'.")
        time.sleep(3)
        # PRESS "SYNTHESIZE"
        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
        print("  ... Pressing the button 'Synthesize'.")
        time.sleep(3)
        # CRAFTING MACRO 1
        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k1"])
        print("  ... Pressing macro 1 ... <wait.{:d}>.".format(json_data["m1"]))
        time.sleep(json_data["m1"])
        # CRAFTING MACRO 2
        app.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k2"])
        print("  ... Pressing macro 2 ... <wait.{:d}>.".format(json_data["m2"]))
        time.sleep(json_data["m2"])
except KeyboardInterrupt:
    print("Program has stopped.")
    sys.exit()