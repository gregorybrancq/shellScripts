#!/bin/zsh

# #xrandr --output DVI-I-1 --off
# xrandr --output HDMI-0 --off
# sleep 5s
# #xrandr --auto --output DVI-I-1 --mode 1680x1050 --right-of HDMI-0
# xrandr --auto --output HDMI-0 --mode 1680x1050 --left-of DVI-I-1
#
#cvt 1680 1050 60     pour connaitre les paramètres de la ligne suivante
xrandr --newmode "1680x1050_60.00"  146.25  1680 1784 1960 2240  1050 1053 1059 1089 -hsync +vsync
xrandr --addmode DP-2-1 1680x1050_60.00



gnome-control-center display &
proc_gcc=`ps -C gnome-control-center -o pid=`

sleep 10s

kill -9 $proc_gcc

