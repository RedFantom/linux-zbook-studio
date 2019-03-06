"""
Author: RedFantom
License: GNU GPlv3
Copyright (c) 2019 RedFantom
"""
import signal
import subprocess as sp
import threading
from time import sleep


exit_flag: threading.Event = threading.Event()


def get_device_id(device="HP Wireless hotkeys"):
    # type: (str) -> (str, None)
    """
    Return the xinput device ID for the given device name

    :param device: Name of the device to find the ID for
    :return: ID number of type str
    """
    p = sp.Popen(["xinput", "list"], stdout=sp.PIPE)
    p.wait()
    stdout = p.stdout.read().decode()
    lines = [line for line in stdout.split("\n") if device in line]
    if len(lines) == 0:  # No valid device found
        return None
    id_number = lines[0].split("=")[1][0:3].strip()
    return id_number


def monitor_device(device):
    # type: (sp.Popen, threading.Event) -> None
    """
    Run a loop to monitor the device for keypresses and act on them

    :param device: xinput device ID number
    """
    global exit_flag
    p = sp.Popen(["xinput", "test", device], stdout=sp.PIPE)
    p.stdout.write = lambda s: print("Writing:", s, end="", flush=True)
    buffer = str()
    while not exit_flag.is_set():
        if not p.stdout.readable():
            sleep(0.1)
            continue
        buffer += p.stdout.read(1).decode()
        if "key press" in buffer:  # Key has been pressed
            print(buffer)
            buffer = str()
            toggle_wifi()


def toggle_wifi():
    # type: () -> None
    """Toggle the state of the WiFi"""
    state = get_wifi_status()
    sp.call(["nmcli", "radio", "wifi", "on" if not state else "off"])


def get_wifi_status():
    # type: () -> bool
    """Determine the current WiFi status (on/off) using rfkill"""
    p = sp.Popen(["nmcli", "radio", "wifi"], stdout=sp.PIPE)
    p.wait()
    stdout = p.stdout.read().decode()
    return "enabled" in stdout


def setup_keycode():
    """Set the appropriate keycode for the WiFi Button"""
    sp.call(["setkeycodes", "e078", "246"])


def main():
    """Run the daemon to control the Wi-Fi"""
    id_number = get_device_id()
    if id_number is None:
        print("Failed to determine device ID number")
        exit(-1)
    monitor_device(id_number)
    exit(0)


def signal_handler(num, frame):
    """Handle a termination signal"""
    global exit_flag
    exit_flag.set()
    print("Exiting hotkeys...", flush=True)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
