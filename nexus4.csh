#!/bin/tcsh -f

set mountDir="/media/Nexus 4"
#set mountDir="/media/MyAndroid"

set mntExist=`ls "$mountDir"`

if ($#mntExist == "0") then
    #mtpfs -o allow_other "$mountDir"
    go-mtpfs "$mountDir"
    sleep 1
else
    fusermount -u "$mountDir"
endif

