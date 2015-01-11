#!/usr/bin/env python

'''
Turn images depends on the EXIF information
'''



## Import
import sys
import os
import re
import time, datetime
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
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

parser.add_option(
    "--nogui",
    action  = "store_false",
    dest    = "gui",
    default = True,
    help    = "Print information in a shell"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def exifConvert(photoList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  exifConvert")

    oldDir = os.getcwd()

    for (photoD, photoN, photoE) in photoList :
        dbg.info(HEADER, "In  exifConvert directory " + str(photoD) + "  convert " + photoN + photoE)

        if (photoD != "") :
            os.chdir(photoD)

        procPopen = subprocess.Popen('exifautotran "' + photoN + photoE + '"', shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            dbg.warn(HEADER, "In  exifConvert file " + str(os.path.join(photoD, photoN + photoE)) + " was not turned.")

        if (photoD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out exifConvert")

###############################################






###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global dbg
    warnC = 0
    dbg.info(HEADER, "In  main")

    photoList = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".JPG", ".jpg", ".JPEG", ".jpeg"]
    (photoList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one photo to unpack
    if (len(photoList) == 0) :
        dialog_error("Pivoter les images", "\nNo photo has been found\n")
    else :
        dbg.info(HEADER, "In  main photo to convert = " + str(len(photoList)))

    ## Convert them
    exifConvert(photoList)

    ## End dialog
    dialog_end(warnC, errC, logFile, "Pivoter les images", "\nJob fini : " + str(len(photoList)) + " images converties.")
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


