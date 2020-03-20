#!/bin/sh -f

lsb_release -a

echo "Kernel name:   " `uname -s`
echo "Kernel release:" `uname -r`
echo "Processor:     " `uname -p`
echo "32 or 64 bits: " `getconf LONG_BIT`
echo "OS:            " `uname -o`

