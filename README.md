## i3-shutdown
This program calls 'i3-msg exit' after cleanly shutting down all windows.

i3 kills processes when invoking the 'exit' command instead of cleanly shutting them down. This project aims to provide an application for gracefully closing the x11 windows associated with the applications and waiting for them to close. The user can either force quit the window manager or cancel the exit operation if an application needs attention and is notified of the windows waiting to be closed.

# Usage
Edit your i3 configuration file and assign the [i3-shutdown.py](https://github.com/vetux/i3-graceful-exit/blob/master/i3-graceful-exit.py) script as the action of the i3nagbar you use to quit the application replacing <code>i3-msg quit</code> (Default set to $mod+Shift+e) and add <code>for_window [class="i3-shutdown"] fullscreen enable"</code> to run the shutdown dialog in fullscreen or alternatively <code>for_window [class="i3-shutdown"] floating enable"</code> for a floating dialog.

# Dependencies
- [python-xlib](https://github.com/python-xlib/python-xlib)
- PyQt5
- xdotool
- wmctrl
