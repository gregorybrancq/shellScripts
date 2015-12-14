#!/bin/tcsh -f

####################################### 
###   MISE A JOUR DE ipfilter.dat   ###
#######################################

cd ~/.azureus/tmp

# Téléchargement du fichier au format rar
wget -N http://emulepawcio.sourceforge.net/ipfilter.rar

# Extraction du fichier
unrar e ipfilter.rar

# Retrait des commentaires pour que le fichier soit reconnu
grep -v '^#' ipfilter.dat > ../ipfilter.dat
rm ipfilter.dat

