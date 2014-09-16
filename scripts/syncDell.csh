#!/bin/tcsh -f

set mntExist=`ls /mnt/Portable/`

if ($#mntExist == "0") then
    mount /mnt/Portable/
    sleep 1
    set mntExist=`ls /mnt/Portable/`
    if ($#mntExist != "0") then
        unison-gtk -links false Portable &
    endif
else
    umount /mnt/Portable/
endif

