#!/bin/sh -f

lsb_release -a

echo "32 or 64 bits: " `getconf LONG_BIT`

