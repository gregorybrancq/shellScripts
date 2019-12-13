#!/bin/sh -f

switch=1

# Determine which interface is playing
defSink=`pacmd list-sinks | grep -e 'name:' -e 'index' | grep "*" | awk -F "index: " '{print $NF}'`
echo "defSink = $defSink"

if [ $PORTABLE -eq 1 ] ; then
    sabreSink=`pactl list short sinks | grep -i "sabre" | awk -F " " '{print $1}'`
    echo "sabreSink = $sabreSink"
    speakerSink=$sabreSink
    headSink=`pactl list short sinks | grep -i "analog-stereo" | grep -i "pci" | grep -v "home" | awk -F " " '{print $1}'`
    echo "headSink = $headSink"
else
    dacSink=`pactl list short sinks | grep -i "focal" | awk -F " " '{print $1}'`
    echo "dacSink = $dacSink"
    speakerSink=$dacSink
    headSink=`pactl list short sinks | grep -vi "focal" | awk -F " " '{print $1}'`
    echo "headSink = $headSink"
fi


# Check if all opened sinks are on default
for sink in `pactl list short sink-inputs | awk -F " " '{print $2}'` ; do
    echo "Sink = $sink"
    indexSink=`echo $sink | awk -F " " '{print $1}'`
    outputSink=`echo $sink | awk -F " " '{print $2}'`
    if [ $sink -ne $defSink ] ; then
        switch=0
    fi
done


# Get back opened sinks
defIndexS=`pactl list short sink-inputs | awk -F " " '{print $1}'`
echo "defIndexS = $defIndexS%"
echo "switch = $switch%"
echo "defSink = $defSink%"
echo "headSink = $headSink%"
echo "speakerSink = $speakerSink%"
echo "PORTABLE = $PORTABLE%"


# Initialize audio
if [ $switch -eq 0 ] ; then
    winTitle="Initialize Audio"
    winText=""
    winIcon="audio-card"
    #echo $winText

    # For all opened sinks
    for defIndex in $defIndexS; do
        echo "defIndex=$defIndex to $defSink"
        pacmd move-sink-input $defIndex $defSink
    done

# Switch to Speakers
elif [ $defSink -eq $headSink ] ; then
    if [ $PORTABLE -eq 1 ] ; then
        # Audiophonics Sabre
        winTitle="Audiophonics U_Sabre"
        winText="Switch audio to U_Sabre"
        winIcon="audio-speakers"
    else
        # Focal XS
        winTitle="Focal XS"
        winText="Switch audio to speakers"
        winIcon="audio-speakers"
    fi
    #echo $winText
    
    pacmd set-default-sink $speakerSink
    # For all opened sinks
    for defIndex in $defIndexS; do
        echo "defIndex=$defIndex to $speakerSink"
        pacmd move-sink-input $defIndex $speakerSink
    done

# Switch to Headphones
elif [ $defSink -eq $speakerSink ] ; then
    winTitle="Sennheiser HD598"
    winText="Switch audio to headphones"
    winIcon="audio-headphones"
    #echo $winText
    
    # Headphones
    pacmd set-default-sink $headSink
    # For all opened sinks
    for defIndex in $defIndexS; do
        echo "defIndex=$defIndex to $headSink"
        pacmd move-sink-input $defIndex $headSink
    done

fi

# Notification
# due to a bug, the timer doesn't work https://bugs.launchpad.net/ubuntu/+source/notify-osd/+bug/390508
# so sleep and kill
notify-send --urgency=critical --icon=$winIcon "$winTitle" "$winText" ; sleep 2 ; killall notify-osd &

