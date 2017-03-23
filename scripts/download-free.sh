#!/bin/zsh


urlFichier=$1


if test $# != 1
then
    echo -e "Telechargeur de fichier heberge sur dl.free.fr\n"
    echo -e "Tips par Danux et mis en forme par SnakemaN\n"
    echo -e "USAGE : download-free <url du fichier a telecharger>\n"
else
    echo -e "Telechargement du fichier $1"

    wget -c $urlFichier

    #dt=`date +%Y-%m-%d_%H:%M:%S.%N`
    #cookie="/tmp/cookie$dt.txt"
    #tmpFile="/tmp/cookie$dt.txt"

    ##First step is set cookie
    #wget --save-cookies $cookie --keep-session-cookies $urlFichier -O $tmpFile
    #
    ##Second step is retry with cookie
    #wget -c --load-cookies $cookie $urlFichier
    #
    ##Then clean tmp file
    #rm -rf $tmpFile $cookie

fi
