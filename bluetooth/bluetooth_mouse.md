# Bluetooth Mouse
When trying to pair a Bluetooth mouse with a laptop under Ubuntu, you might
encounter a variety of problems. Note again that all of these solutions
are only tested under Ubuntu 17.10 running GNOME.

## Mouse not pairing
If your Bluetooth mouse is not pairing, or seems to pair but you cannot move
the cursor with it, then you could try changing the pairing mode to `simple`
using this command:
```bash
hciconfig hci0 sspmode 1
```
If the command fails, check if `hci0` is the correct identifier for your 
Bluetooth device with the command `hciconfig` (just like `ifconfig`). Then
apply the setting by restarting your Bluetooth device:
```bash
hciconfig hci0 down
hciconfig hci0 up
```
If this does not fix the problem, and you want to reset to the previous state,
simply disable simple pairing mode again:
```bash
hciconfig hci0 sspmode 0
```
Then you can try another solution if you can find one.

Source: [Eric's Blog](https://ericasberry.com/blog/2016/09/30/pairing-a-logitech-mx-master-mouse-with-ubuntu-16-04-using-bluetooth/)

## Mouse not re-connecting
If your Bluetooth mouse disconnects when your laptop goes to sleep and does not
re-connect afterwards without being manually connected using the Bluetooth
settings, you could try creating a script that is automatically run when
your laptop goes to sleep and resumes.

Create a file named `/etc/pm/sleep.d/bluetooth` (or another file name if you
prefer, as long as it's in that folder), and insert the following:
```bash
#!/bin/bash

. /usr/lib/pm-utils/functions

case "$1" in
    hibernate|suspend)
    rfkill block bluetooth
    ;;
    thaw|resume)
    rfkill unblock bluetooth
    ;;
    *)
    ;;
esac

exit
```

After making sure that it's runnable (`sudo chmod +x bluetooth`), reboot and 
now your mouse should re-connect automatically!

Source: [Ferux's answer on the Ubuntu Forums](https://ubuntuforums.org/showthread.php?t=1387211&p=8728266#post8728266)
