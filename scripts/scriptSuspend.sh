#!/bin/sh

# this script must be linked here by root user
# ln -s /home/greg/Greg/work/env/bin/scriptSuspend /lib/systemd/system-sleep/

export DISPLAY=:0.0
export XAUTHORITY=/home/greg/.Xauthority

case $1 in
    pre)
        ;;
    post)
        /home/greg/Greg/work/env/bin/dodoJuju
        ;;
esac
