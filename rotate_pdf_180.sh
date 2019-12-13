#!/bin/sh
for i in *.pdf; 
    do echo $i && pdftk $i cat 1-endD output tmp/${i};
done
