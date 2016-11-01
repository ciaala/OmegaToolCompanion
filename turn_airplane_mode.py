#!/usr/bin/env python3

from subprocess import run
from time import sleep

message_already_front = """Starting: Intent { act=android.settings.AIRPLANE_MODE_SETTINGS }
Warning: Activity not started, its current task has been brought to the front"""


command_click_enable = ["adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS", "adb shell input keyevent 23", "adb shell input keyevent 61", "adb shell input keyevent 66"]
command_click_disable = ["adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS", "adb shell input keyevent 23"]
command_click_exit = ["adb shell input keyevent 4"]

adb_path = "/Users/crypt/Library/Android/sdk/platform-tools/adb"


def run_shell_command(command):
    """
    run a shell command

    :type command: str
    :param command:


    :return:
    """
    tokens = command.split(' ')
    if tokens[0] == "adb":
        tokens[0] = adb_path
    out = run(tokens)
    sleep(0.7)
    #, stdin=sin, stdout=sout, stderr=subprocess.STDOUT)

def run_shell_commands(commands):
    for command in commands:
        run_shell_command(command)


def android_airplane_mode_toggler():
    run_shell_commands(command_click_enable)
    #run_shell_commands(command_click_exit)
    sleep(3)
    run_shell_commands(command_click_disable)
    run_shell_commands(command_click_exit)


if __name__ == "__main__":
    run_shell_commands(command_click_exit)
    while True:
        print("start loop")
        android_airplane_mode_toggler()
        print("end loop")
        sleep(20)