#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Reduce photo size
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "photoReduce"

## directory
logDir = getLogDir()

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
resizePercent = 100
winTitle = "Reduce photo size"

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def reduceFile(fileList) :
    global log
    global errC
    log.info(HEADER, "In  reduceFile")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        log.info(HEADER, "In  reduceFile directory " + str(fileD) + "  reduceFile " + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='mogrify -resize ' + str(resizePercent) + '% ' + fileN + fileE
        log.info(HEADER, "In  reduceFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            log.error(HEADER, "In  reduceFile file: issue with " + str(os.path.join(fileD, fileN + fileE)))

        if (fileD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out reduceFile")

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
    global resizePercent
    warnC = 0
    log.info(HEADER, "In  main")

    fileList = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        log.exit("Reduce photo size", "No image has been found\n")
    else :
        resizePercentStr = MessageDialog(type_='entry', title=winTitle, message="Quelle est le pourcentage de réduction ?").run()
        try :
            resizePercent=int(resizePercentStr)
        except ValueError :
            MessageDialog(type_='error', title=winTitle, message="\nle pourcentage doit être un chiffre entre 0 et 100.\n").run()
            log.exit(HEADER, "In  main resizePercent is not an integer")

    ## Convert them
    log.dbg("fileList="+str(fileList))
    reduceFile(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, winTitle, "\nJob fini.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)
    main()


