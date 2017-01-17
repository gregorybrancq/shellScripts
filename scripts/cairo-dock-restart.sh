#!/bin/sh -f

proc=`ps -C cairo-dock -o pid=`

echo "Kill cairo-dock (process $proc)"
kill -9 $proc

echo "Launch new cairo-dock"
cairo-dock &


