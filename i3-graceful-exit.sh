#!/bin/bash

# Depends on xdotool and wmctrl

allWindows=$(xdotool search -onlyvisible "" 2> /dev/null)

echo "$allWindows" | while IFS= read -r line ; do
	killWindow=0
	if [ "$line" != "$focus" ]
	then
		wmctrl -ci "$line"
	fi
done

# TODO: Wait and give user option to skip waiting
sleep 1s

i3-msg exit
