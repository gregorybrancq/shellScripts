#!/bin/sh -f

#
# Run through gnome-schedule
#   - 5 workdays from 23h45 to 6h.
#
# Functionalities :
#   - Kill programs
#   - Blocks keyboard and mouse
# 

progName=$(basename "$0")

# Log file
logE=0
logF="$HOME/Greg/work/env/log/${progName}_`date +%Y-%m-%d_%H:%M:%S.%N`.log"

# Enable
progEnable=1
block=0
unblock=0

# To have these informations :
#   > xinput -list
keyboardId=9
mouse1Id=10
mouse2Id=11

# Programs list
prgs="totem vlc mplayer smplayer rhythmbox amarok"

# Sleep Interval (in min)
sleepInterval="5"

# Day, Hour, Min
# begin and end must not be the same number !
beginDay=1
endDay=4
beginDayTime="2345"
endDayTime="0600"

beginWeek=5
endWeek=7
beginWeekTime="0100"
endWeekTime="0700"



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
checkDayHour() {
    curDay=`date +%u`
    curTime=$(date +"%H%M" | bc)

    if [ $logE -eq 1 ]; then
        echo "`date`" >> $logF
        echo "Day=$curDay Time=$curTime" >> $logF
    fi

    # Check day
    inDay=0
    if [ $curDay -ge $beginDay ] && [ $curDay -le $endDay ]; then
        inDay=1

        # defined good time
        beginTime=$beginDayTime
        endTime=$endDayTime

        # defined time to unlock (endTime + 3xslepInterval)
        endExtraTime=`expr $endDayTime + 3 * $sleepInterval`

    elif [ $curDay -ge $beginWeek ] && [ $curDay -le $endWeek ]; then
        inDay=1

        # defined good time
        beginTime=$beginWeekTime
        endTime=$endWeekTime

        # defined time to unlock (endWeekTime + 3xslepInterval)
        endExtraTime=`expr $endWeekTime + 3 * $sleepInterval`

    fi

    # Check hour
    inInter=0
    afterInter=0
    if [ $inDay -eq 1 ]; then

        if [ $beginTime -le $endTime ]; then
            if [ $curTime -ge $beginTime ] && [ $curTime -le $endTime ]; then
                inInter=1
            elif [ $curTime -ge $beginTime ] && [ $curTime -le $endExtraTime ]; then
                afterInter=1
            fi
        else
            if [ $curTime -ge $beginTime ] || [ $curTime -le $endTime ]; then
                inInter=1
            elif [ $curTime -ge $beginTime ] || [ $curTime -le $endExtraTime ]; then
                afterInter=1
            fi
        fi

    fi

    # Compute
    if [ $inInter -eq 1 ]; then
        if [ $logE -eq 1 ]; then
            echo "In interval beginTime=$beginTime < curTime=$curTime < endTime=$endTime" >> $logF
        fi
        return 1
    elif [ $afterInter -eq 1 ]; then
        if [ $logE -eq 1 ]; then
            echo "After interval beginTime=$beginTime < curTime=$curTime < endExtraTime=$endExtraTime" >> $logF
        fi
        return 2
    else
        if [ $logE -eq 1 ]; then
            echo "Out interval curTime=$curTime, beginTime=$beginTime < endTime=$endTime" >> $logF
        fi
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
    xinput disable $mouse1Id
    xinput disable $mouse2Id
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
    xinput enable $mouse1Id
    xinput enable $mouse2Id
    #xinput set-prop $mouseId "Device Enabled" 1
    if [ $logE -eq 1 ]; then
        echo "End unblock keyboard & mouse" >> $logF
    fi
}



#
# Main script
#

if [ $progEnable -eq 1 ]; then

    while [ 1 ]
    do

        # Check if the day/hour allows to execute
        checkDayHour
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

        fi

        sleep ${sleepInterval}m

    done
fi

