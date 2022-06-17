## i3-graceful-exit
This program calls 'i3-msg exit' after cleanly shutting down all windows.

i3 kills processes when invoking the 'exit' command instead of cleanly shutting them down. This project aims to solve the problem by gracefully closing the x11 windows associated with the applications and waiting for them to close. The user can either force quit the window manager or cancel the exit operation if an application needs attention and is notified of the windows waiting to be closed.

# Usage
Assign the [i3-graceful-exit.py](https://github.com/vetux/i3-graceful-exit/blob/master/i3-graceful-exit.py) script as the action of the i3nagbar you use to quit the application replacing 'i3-msg quit' (Default set to $mod+Shift+e)

# Dependencies
- [python-xlib](https://github.com/python-xlib/python-xlib)
- PyQt5
- xdotool
- wmctrl
