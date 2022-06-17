## i3-graceful-exit
i3 kills processes when invoking the 'exit' command instead of cleanly shutting them down. This project aims to solve the problem by gracefully closing the x11 windows associated with the applications and waiting for them to close. The user can either force quit the window manager or cancel the exit operation if an application needs attention.

# Dependencies
- [python-xlib](https://github.com/python-xlib/python-xlib)
- PyQt5
- xdotool
- wmctrl
