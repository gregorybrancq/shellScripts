#!/bin/sh -f

# Determine which interface is playing
defSink=`pacmd list-sinks | grep -e 'name:' -e 'index' | grep "*" | awk -F "index: " '{print $NF}'`
echo "defSink = $defSink"
# Get back open sinks
defIndexS=`pacmd list-sink-inputs | grep 'index' | awk -F 'index: ' '{print $NF}'`
echo "defIndexS = $defIndexS"


# Switch audio interface
if [ $defSink -eq 0 ] ; then
    echo "Switch to Focal"
    # Focal XS
    pacmd set-default-sink 1
    # For all open sink
    for defIndex in $defIndexS; do
        pacmd move-sink-input $defIndex 1
    done
else
    echo "Switch to Headphone"
    # Headphones
    pacmd set-default-sink 0
    # For all open sink
    for defIndex in $defIndexS; do
        pacmd move-sink-input $defIndex 0
    done
fi

