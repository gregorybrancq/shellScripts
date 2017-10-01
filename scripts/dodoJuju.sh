#!/bin/sh -f

#
# Run through gnome-schedule
#   - 5 workdays from 1h to 6h.
#
# Functionalities :
#   - Kill mplayer and vlc
#   - Blocks keyboard and mouse
# 

progName=$(basename "$0")

# Log file
logE=0
logF="$HOME/Greg/work/env/log/$progName_`date +%Y-%m-%d_%H:%M:%S.%N`.log"

# Enable
progEnable=1
block=0
unblock=0

# To have these informations :
#   > xinput -list
keyboardId=10
mouseId=9

# Programs list
prgs="totem vlc mplayer rhythmbox"

# Day & Hour
beginDay=1
endDay=7
beginHour=0
endHour=6

if [ $logE -eq 1 ]; then
    echo " Main script $progName\n" > $logF
fi



# 
# Args
#

for i in "$@"
do
case $i in
    -b|--block)
    block=1
    if [ $logE -eq 1 ]; then
        echo "Block option" >> $logF
    fi
    shift # past argument=value
    ;;
    -u|--unblock)
    unblock=1
    if [ $logE -eq 1 ]; then
        echo "Unblock option" >> $logF
    fi
    shift # past argument=value
    ;;
    -h|--help)
    echo "**********\n** HELP **\n**********"
    echo " -b|--block     block the keyboard and mouse"
    echo " -u|--unblock   unblock the keyboard and mouse"
    exit 0
    ;;
    *)
            # unknown option
    ;;
esac
done



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
    if [ $logE -eq 1 ]; then
        echo "`date`" >> $logF
        echo "Day=$day Hour=$hour Min=$min" >> $logF
    fi

    beginDayTmp=`expr $beginDay - 1`
    endDayTmp=`expr $endDay + 1`
    beginHourTmp=`expr $beginHour - 1`
    if [ $logE -eq 1 ]; then
        echo "beginDay=$beginDayTmp endDay=$endDayTmp beginHour=$beginHourTmp endHour=$endHour" >> $logF
    fi

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
    if [ $logE -eq 1 ]; then
        echo "Kill progs" >> $logF
    fi
    for prog in $prgs
    do
        # Get id
        proc=`ps -C $prog -o pid=`
        
        # Kill it
        if [ "$proc" != "" ]; then
            if [ $logE -eq 1 ]; then
                echo "Prog $prog with pid $proc has been killed." >> $logF
            fi
            kill -9 $proc        
        fi
    done
}


blockKbMouse() {
    if [ $logE -eq 1 ]; then
        echo "Begin block keyboard & mouse" >> $logF
    fi
    xinput disable $keyboardId
    #xinput set-prop $keyboardId "Device Enabled" 0
    xinput disable $mouseId
    #xinput set-prop $mouseId "Device Enabled" 0
    if [ $logE -eq 1 ]; then
        echo "End block keyboard & mouse" >> $logF
    fi
}


unblockKbMouse() {
    if [ $logE -eq 1 ]; then
        echo "Begin unblock keyboard & mouse" >> $logF
    fi
    xinput enable $keyboardId
    #xinput set-prop $keyboardId "Device Enabled" 1
    xinput enable $mouseId
    #xinput set-prop $mouseId "Device Enabled" 1
    if [ $logE -eq 1 ]; then
        echo "End unblock keyboard & mouse" >> $logF
    fi
}



#
# Main script
#

if [ $progEnable -eq 1 ]; then

    # Check if the date/hour allows to execute
    checkDateHour
    varDH=$?
    if [ $logE -eq 1 ]; then
        echo "varDH = $varDH" >> $logF
    fi

    if [ $block -eq 1 ]; then
        if [ $logE -eq 1 ]; then
            echo "Block" >> $logF
        fi

        # Block keyboard and mouse
        blockKbMouse

    elif [ $varDH -eq 2 ] || [ $unblock -eq 1 ]; then
        if [ $logE -eq 1 ]; then
            echo "Unblock" >> $logF
        fi

        # Unblock keyboard and mouse
        unblockKbMouse

    elif [ $varDH -eq 1 ]; then
        if [ $logE -eq 1 ]; then
            echo "Kill and block" >> $logF
        fi

        # Kill the different programs
        killPrgs

        # Block keyboard and mouse
        blockKbMouse

    else
        if [ $logE -eq 1 ]; then
            echo "Do nothing" >> $logF
        fi

    fi
fi

