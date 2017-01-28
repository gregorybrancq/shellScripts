#!/bin/sh -f

# process cairo-dock
proc_cd=`ps -C cairo-dock -o pid=`

# process cairo-dock-launcher-API-daemon
proc_cdlad=`ps -C "python /usr/lib/x86_64-linux-gnu/cairo-dock/cairo-dock-launcher-API-daemon" -o pid=`

echo "Kill cairo-dock (process $proc_cd)"
kill -9 $proc_cd
echo "Kill cairo-dock-launcher-API-daemon (process $proc_cdlad)"
kill -9 $proc_cdlad

echo "Launch new cairo-dock"
cairo-dock &


