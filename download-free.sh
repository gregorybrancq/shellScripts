#!/bin/zsh


urlFile=$1
renameFile=$2
urlNameFile=`basename $urlFile`

if test $# != 2
then
    echo -e "Telechargeur de fichier heberge sur dl.free.fr\n"
    echo -e "Tips par Danux et mis en forme par SnakemaN\n"
    echo -e "USAGE : download-free <url du fichier a telecharger> <file name>\n"
else
    echo -e "Telechargement du fichier $1 (cookie)"

    dt=`date +%Y-%m-%d_%H:%M:%S.%N`
    cookie="/tmp/cookie$dt.txt"
    tmpFile="/tmp/cookie$dt.txt"

    #First step is set cookie
    wget --save-cookies $cookie --keep-session-cookies $urlFile -O $tmpFile
    
    #Second step is retry with cookie
    wget -c --load-cookies $cookie $urlFile
    
    #Then clean tmp file
    rm -rf $tmpFile $cookie

    testFile=`file $urlNameFile | grep "Media"`
    #echo "testFile = $testFile"
    #echo "#testFile = $#testFile"

    if [ $#testFile -eq 0 ]
    then
        rm -f $urlNameFile

        echo -e "Telechargement du fichier $1 (wget)"
        wget -c $urlFile
    fi

    echo -e "Renommer le fichier $1 en $2"
    mv $urlNameFile "$renameFile"
fi
