#!/usr/bin/env python

'''
Turn images depends on the EXIF information
'''



## Import
import sys
import os
import re
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "Photo_Turn"

## directory
logDir   = getLogDir()

###############################################



###############################################
###############################################
##              Line Parsing                 ##
###############################################
###############################################

parsedArgs = {}
parser = OptionParser()


parser.add_option(
    "-d",
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def exifConvert(photoList) :
    global log
    global errC
    log.info(HEADER, "In  exifConvert")

    oldDir = os.getcwd()

    for (photoD, photoN, photoE) in photoList :
        log.info(HEADER, "In  exifConvert directory " + str(photoD) + "  convert " + photoN + photoE)

        if (photoD != "") :
            os.chdir(photoD)

        procPopen = subprocess.Popen('exifautotran "' + photoN + photoE + '"', shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            log.warn(HEADER, "In  exifConvert file " + str(os.path.join(photoD, photoN + photoE)) + " was not turned.")

        if (photoD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out exifConvert")

###############################################






###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global log
    warnC = 0
    log.info(HEADER, "In  main")

    photoList = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".JPG", ".jpg", ".JPEG", ".jpeg"]
    (photoList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one photo to unpack
    if (len(photoList) == 0) :
        MessageDialog(type_='error', title="Pivoter les images", message="\nNo photo has been found\n").run()
    else :
        log.info(HEADER, "In  main photo to convert = " + str(len(photoList)))

    ## Convert them
    exifConvert(photoList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Pivoter les images", "\nJob fini : " + str(len(photoList)) + " images converties.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


