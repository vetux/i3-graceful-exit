#!/bin/bash

# i3 by default kills all the processes which were started through the gui when exiting the window manager.
# This script closes all visible windows gracefully (The same as clicking the x on a more conventional window manager) before exiting i3.
# It should be assigned in .config/i3/config as the exit shortcut nagbar click action instead of 'i3-msg exit'

# Depends on xdotool and wmctrl

allWindows=$(xdotool search -onlyvisible "" 2> /dev/null)

echo "$allWindows" | while IFS= read -r line ; do
	wmctrl -ci "$line"
done

# TODO: Wait and give user option to skip waiting
sleep 1s

i3-msg exit
