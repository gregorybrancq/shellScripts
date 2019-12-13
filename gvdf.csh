#!/bin/tcsh -f

set getInfo="0"
set put="0"
set putMerge="0"
set get="0"
set getMerge="0"


#---------------------------------------------------------------------------#
# Args Test                                                                 #
#---------------------------------------------------------------------------#

while ($#argv)
    switch("$1")

        case "-i":
        case "--info":
            set getInfo="1"
            breaksw

        case "-p":
        case "--put":
            set put="1"
            breaksw

        case "-pm":
        case "--putMerge":
            set putMerge="1"
            breaksw

        case "-g":
        case "--get":
            set get="1"
            breaksw

        case "-gm":
        case "--getMerge":
            set getMerge="1"
            breaksw

        case "-h":
        case "--help":
            USAGE:
            echo "#----------------------------------------------------------------------------#";
            echo "#   The options are:"
            echo "#      -i/--getInfo       -- print the ftp information"
            echo "#      -p/--put           -- put the local dir to the web"
            echo "#      -pm/--putMerge     -- copy the local version to the web directory"
            echo "#      -g/--get           -- get the web to the local dir"
            echo "#      -gm/--getMerge     -- copy the web version to local directory"
            echo "#      -h/--help          -- display this help"
            echo "#----------------------------------------------------------------------------#";
            breaksw
    endsw
    shift
end


if ($?DELL) then
    cd $HOME/Perso/work/gvdf
else
    cd $HOME/Greg/work/gvdf
endif

if ($getInfo) then
    echo "\nGVDF FTP : ftp.grands-vins-de-france.fr"
    echo "login    : grandsvi"
    echo "password : 9XRsz4dd\n"
endif

if ($putMerge) then
    rm -rf ftp.grands-vins-de-france.fr/www
    cp -r local/* ftp.grands-vins-de-france.fr/
    rm -rf ftp.grands-vins-de-france.fr/www/.git
    find ftp.grands-vins-de-france.fr -iname '*.swp' -exec rm -rf '{}' ';'
endif

if ($put) then
    cd ftp.grands-vins-de-france.fr
    wput www ftp://grandsvi:9XRsz4dd@ftp.grands-vins-de-france.fr//
    cd ..
endif

if ($get) then
    wget -r -np --user grandsvi --password 9XRsz4dd ftp://ftp.grands-vins-de-france.fr//www/ ~/Greg/work/gvdf/
endif

if ($getMerge) then
    cp -r ftp.grands-vins-de-france.fr/www local/
endif



