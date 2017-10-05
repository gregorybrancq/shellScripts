#!/bin/sh -f

# Determine which interface is playing
defSink=`pacmd list-sinks | grep -e 'name:' -e 'index' | grep "*" | awk -F "index: " '{print $NF}'`
defIndex=`pacmd list-sink-inputs | grep "index"  | awk -F "index: " '{print $NF}'`

# Switch audio interface
if [ $defSink -eq 0 ] ; then
    echo "Switch to Focal"
    # Focal XS
    pacmd set-default-sink 1 && pacmd move-sink-input $defIndex 1
else 
    echo "Switch to Headphone"
    # Headphones
    pacmd set-default-sink 0 && pacmd move-sink-input $defIndex 0
fi

