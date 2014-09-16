#/bin/tcsh -f

#gconftool-2 -s "/apps/gnome-power-manager/backlight/idle_dim_ac" False -t boolean 
#gconftool-2 -s "/apps/gnome-power-manager/buttons/suspend" "suspend" -t string 
#gconftool-2 -s "/apps/gnome-power-manager/buttons/power" "shutdown" -t string 
#gconftool-2 -s "/apps/gnome-power-manager/buttons/lid_ac" "nothing" -t string 
#gconftool-2 -s "/apps/gnome-power-manager/disks/spindown_enable_ac" False -t boolean 
#gconftool-2 -s "/apps/gnome-power-manager/disks/spindown_enable_battery" False -t boolean 
#gconftool-2 -s "/apps/gnome-power-manager/lock/suspend" False -t boolean 
#gconftool-2 -s "/apps/gnome-power-manager/lock/hibernate" False -t boolean
xset dpms force off
xset -display :0 s off -dpms
