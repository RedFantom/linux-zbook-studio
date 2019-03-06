# HotKeys

## Mute Button
Create a new file named `/etc/modprobe.d/alsa-base.conf` and insert
```
options snd-hda-intel model=mute-led-gpio
```
to make the LED of the Mute button work properly. Requires a reboot to
take effect.

## WiFi Button
Enable the use of the WiFi button under a desktop manager that does not
support its behaviour by default using the `hotkeys.py` script. Note 
that the LED is not exposed by the kernel and thus cannot be used.
