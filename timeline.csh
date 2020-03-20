#!/bin/csh -f

set pwdMem=$PWD
cd /opt/timeline/timeline-1.17.0
set nb_args="$#argv"

if ($nb_args != "0") then
    while ($nb_args != 0)
        set file="$argv[$nb_args]"
        if (-f "$file") then
            python timeline.py "$file"
        else
            if (-f "$pwdMem/$file") then
                python timeline.py "$pwdMem/$file"
            else
                echo "File $file doesn't exist"
            endif
        endif
        set nb_args=`expr $nb_args - 1`
    end
else
    python source/timeline.py
endif
