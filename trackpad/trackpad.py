"""
Author: RedFantom
License: MIT
Copyright (C) 2018 RedFantom

Simple Python script to turn off  the Trackpad on a HP Zbook Studio device.
Written for and tested on a Zbook Studio G4, but the G3 has the same trackpad
so it should work as well. If not, then a small modification to the trackpad
device string should do the trick.

Designed to be run with Python 3 and a keyboard hotkey.
"""
import subprocess as sub

"""
String containing the name of the trackpad to disabled.

Author's note: This string works for my specific machine, running Ubuntu 17.10
with GNOME. I cannot guarantee that this name is not device specific. A more
general name is given when using `xinput list` ("AlpsPS/2 ALPS GlidePoint"),
but disabling that device has no effect at all.
"""
TRACKPAD = "ALP0012:00 044E:120C"

if __name__ == '__main__':
    # This not a library, and should not be imported

    # Open a subprocess for `xinput list` to determine whether the trackpad is
    # enabled or disabled
    command = ["xinput", "list", TRACKPAD]
    xinput_list = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE)
    stderr = xinput_list.stderr.read()
    # Check if the output reports that the device does not exist
    if b"unable to find device" in stderr:
        print("[TRACKPAD] `xinput list` could not find device specified")
        exit(-1)
    # Now check if the device is enabled or not
    disabled = b"This device is disabled" in xinput_list.stdout.read()
    # Generate the new command to change the device state
    command = ["xinput", "enable" if disabled else "disable", TRACKPAD]
    xinput = sub.Popen(command, stdout=sub.PIPE).stdout.read()
    if xinput != b"":
        print("[TRACKPAD] `xinput` encountered an error:", xinput)
        exit(-2)
    exit(0)

