#!/bin/sh -f

#
# Run through gnome-schedule
#   - 5 workdays from 1h to 6h.
#
# Functionalities :
#   - Kill mplayer and vlc
#   - Blocks keyboard and mouse
# 

# Log file
logF="/home/greg/Greg/work/env/log/dodoJuju_`date +%Y-%m-%d:%H:%m:%S.%N`.log"

# Enable
enable=1
block=0
unblock=0

# To have these informations :
#   > xinput -list
keyboardId=10
mouseId=9

# Programs list
prgs="totem vlc mplayer"

# Day & Hour
beginDay=1
endDay=5
beginHour=1
endHour=6



# 
# Args
#

for i in "$@"
do
case $i in
    -b|--block)
    block=1
    shift # past argument=value
    ;;
    -u|--unblock)
    unblock=1
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
    echo "Day=$day Hour=$hour Min=$min" >> $logF

    beginDayTmp=`expr $beginDay - 1`
    endDayTmp=`expr $endDay + 1`
    beginHourTmp=`expr $beginHour - 1`
    echo "beginDay=$beginDayTmp endDay=$endDayTmp beginHour=$beginHourTmp endHour=$endHour" >> $logF

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
    echo "Kill progs" >> $logF
    for prog in $prgs
    do
        # Get id
        proc=`ps -C $prog -o pid=`
        
        # Kill it
        if [ "$proc" != "" ]; then
            echo "Prog $prog with pid $proc has been killed." >> $logF
            kill -9 $proc        
        fi
    done
}


blockKbMouse() {
    echo "Block keyboard & mouse" >> $logF
    xinput disable $keyboardId
    xinput disable $mouseId
}


unblockKbMouse() {
    echo "Unblock keyboard & mouse" >> $logF
    xinput enable $keyboardId
    xinput enable $mouseId
}



#
# Main script
#

if [ $enable -eq 1 ]; then
    echo " Main script $0 " >> $logF

    # Check if the date/hour allows to execute
    checkDateHour
    varDH=$?
    echo "varDH = $varDH" >> $logF
    if [ $varDH -eq 1 ] || [ $block -eq 1 ]; then
        echo "Kill and block" >> $logF

        if [ $varDH -eq 1 ]; then
            # Kill the different programs
            killPrgs
        fi

        # Block keyboard and mouse
        blockKbMouse

    elif [ $varDH -eq 2 ] || [ $unblock -eq 1 ]; then
        echo "Unblock" >> $logF

        # Unblock keyboard and mouse
        unblockKbMouse

    else
        echo "Do nothing" >> $logF

    fi
fi

