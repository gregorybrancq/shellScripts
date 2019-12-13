#!/bin/tcsh -f


set title=""
set mms=""
set convert="0"


#---------------------------------------------------------------------------#
# Args Test                                                                 #
#---------------------------------------------------------------------------#

while ($#argv)
    switch("$1")
        case "-t":
        case "--title":
            shift
            set var=`echo $1 | cut -c1`
            if ( ("$1" == "") || ("$var" == "-") ) then
               echo "*ERROR* - Option --title need an argument"
               echo ""
               exit 1
            endif
            set title="$1"
            breaksw

        case "-m":
        case "--mms":
            shift
            set var=`echo $1 | cut -c1`
            if ( ("$1" == "") || ("$var" == "-") ) then
               echo "*ERROR* - Option --mms need an argument"
               echo ""
               exit 1
            endif
            set mms="$1"
            breaksw

        case "-c":
        case "--convert":
            set convert="1"
            breaksw

        case "-h":
        case "--help":
            USAGE:
            echo "#----------------------------------------------------------------------------#";
            echo "#   The options are:"
            echo "#      -t/--title <arg>  -- title of the video"
            echo "#      -m/--mms <arg>    -- mms flux"
            echo "#      -c/--convert      -- convert the wmv format to avi"
            echo "#      -h/--help         -- display this help"
            echo "#----------------------------------------------------------------------------#";
            breaksw

    endsw
    shift
end


echo "Title = $title"
echo "MMS = $mms"
echo "Convert = $convert"

if ( ("$title" != "") && ("$mms" != "") ) then
    mplayer -dumpfile ${title}.wmv -dumpstream $mms
endif

if ($convert == "1") then
    mencoder "${title}.wmv" -ofps 23.976 -ovc xvid -oac mp3lame -xvidencopts bitrate=800 -o "${title}.avi"
endif


