#!/bin/zsh

#xrandr --output DVI-I-1 --off
xrandr --output HDMI-0 --off
sleep 5s
#xrandr --auto --output DVI-I-1 --mode 1680x1050 --right-of HDMI-0
xrandr --auto --output HDMI-0 --mode 1680x1050 --left-of DVI-I-1
