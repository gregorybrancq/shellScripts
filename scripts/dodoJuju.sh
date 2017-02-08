#!/bin/sh -f

#
# Run through gnome-schedule
#   - 5 workdays from 1h to 6h.
#
# Functionalities :
#   - Kill mplayer and vlc
#   - Blocks keyboard and mouse
# 


# Enable
enable="1"

# To have these informations :
#   > xinput -list
keyboardId="16"
mouseId="11"

# Programs list
prgs="totem vlc mplayer"

# Day & Hour
beginDay="1"
endDay="5"
beginHour="1"
endHour="6"


# 
# Functions
#

# will return 0 if it's not in the interval
# will return 1 if it's in the interval
# will return 2 during one hour after the interval (to unlock)
checkDateHour() {
    day=`date +%u`
    hour=`date +%H`
    min=`date +%M`
    echo "Day=$day Hour=$hour Min=$min"

    beginDayTmp=`expr $beginDay - 1`
    endDayTmp=`expr $endDay + 1`
    beginHourTmp=`expr $beginHour - 1`
    echo "beginDay=$beginDayTmp endDay=$endDayTmp beginHour=$beginHourTmp endHour=$endHour"

    if [ $day -gt $beginDayTmp ] && [ $day -lt $endDayTmp ]; then
        if [ $hour -gt $beginHourTmp ] && [ $hour -lt $endHour ]; then
            return 1
        elif [ $hour -eq $endHour ]; then
            return 2
        else
            return 0
        fi
    else
        return 0
    fi
}

killPrgs() {
    echo "Kill progs"
    for prog in $prgs
    do
        # Get id
        proc=`ps -C $prog -o pid=`
        
        # Kill it
        if [ "$proc" != "" ]; then
            echo "Prog $prog with pid $proc has been killed."
            kill -9 $proc        
        fi
    done
}


blockKbMouse() {
    echo "Block keyboard & mouse"
    xinput set-prop $keyboardId 'Device Enabled' 0
    xinput set-prop $mouseId 'Device Enabled' 0
}


unblockKbMouse() {
    echo "Unblock keyboard & mouse"
    xinput set-prop $keyboardId 'Device Enabled' 1
    xinput set-prop $mouseId 'Device Enabled' 1
}



#
# Main script
#

if [ $enable -eq 1 ]; then

    # Check if the date/hour allows to execute
    checkDateHour
    varDH=$?
    echo "varDH = $varDH"
    if [ $varDH -eq 1 ]; then
        echo "Kill and block"

        # Kill the different programs
        killPrgs

        # Block keyboard and mouse
        blockKbMouse

    elif [ $varDH -eq 2 ]; then
        echo "Unblock"

        # Unblock keyboard and mouse
        unblockKbMouse

    else
        echo "Do nothing"

    fi
fi

