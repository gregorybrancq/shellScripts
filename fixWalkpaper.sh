#!/bin/sh

# To fix issue with changing wallpaper when reboot

sleep 5s
curDesktop=`xdotool get_desktop`
xdotool set_desktop 1
#dconf read /org/gnome/shell/extensions/walkpaper/workspace-wallpapers
roxterm --hide-menubar --geometry=100x30+350+280 -e "dconf write /org/gnome/shell/extensions/walkpaper/workspace-wallpapers \"['file:///home/greg/Wallpaper/Home/desk_1.jpg', 'file:///home/greg/Wallpaper/Home/desk_2.jpg', 'file:///home/greg/Wallpaper/Home/desk_3.png', 'file:///home/greg/Wallpaper/Home/desk_4.jpg', 'file:///home/greg/Wallpaper/Home/desk_5.jpg']\""
sleep 1s
xdotool set_desktop $curDesktop
