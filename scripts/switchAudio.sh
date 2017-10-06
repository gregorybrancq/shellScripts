#!/bin/sh -f

# Determine which interface is playing
defSink=`pacmd list-sinks | grep -e 'name:' -e 'index' | grep "*" | awk -F "index: " '{print $NF}'`
echo "defSink = $defSink"
defIndex0=`pacmd list-sink-inputs | grep -m1 'index' | awk -F 'index: ' '{print $NF}'`
echo "defIndex0 = $defIndex0"
defIndex1=`pacmd list-sink-inputs | grep -m2 'index' | grep -v "$defIndex0" | awk -F 'index: ' '{print $NF}'`
echo "defIndex1 = $defIndex1"

# Switch audio interface
if [ $defSink -eq 0 ] ; then
    echo "Switch to Focal"
    # Focal XS
    pacmd set-default-sink 1 
    # For video
    pacmd move-sink-input $defIndex1 1 
    # For music
    pacmd move-sink-input $defIndex0 1 
else 
    echo "Switch to Headphone"
    # Headphones
    pacmd set-default-sink 0 
    # For video
    pacmd move-sink-input $defIndex1 0 
    # For music
    pacmd move-sink-input $defIndex0 0 
fi

