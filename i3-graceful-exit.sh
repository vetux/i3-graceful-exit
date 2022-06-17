#!/bin/bash

# Depends on xdotool

focus=$(xdotool getwindowfocus)
allWindows=$(xdotool search -onlyvisible "")

closeWindows=""

echo "$allWindows" | while IFS= read -r line ; do
	killWindow=0
	if [ "$line" != "$focus" ]
	then
               xdotool windowclose "$line"
	fi
done

# TODO: Wait and give user option to skip waiting
sleep 1s

i3-msg exit
