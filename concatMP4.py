#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Convert X mp4 to 1 mp4
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "XMp4TO1Mp4"

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

def concatFile(fileList) :
    global log
    global errC
    log.info(HEADER, "In  concatFile")

    outputFileName = ""
    outputFileExt  = ""
    fileListConcat = ""
    for (fileD, fileN, fileE) in fileList :
        fileDir = ""
        if (outputFileName == "") :
            outputFileName = fileN
            outputFileExt = fileE
        if (fileD != "") :
            fileDir += fileD + "/"

        fileListConcat += '-cat "' + fileDir + fileN + fileE + '" '

    findName = False
    i = 0
    log.info(HEADER, "In  concatFile outputFileName=" + str(outputFileName) + " outputFileExt=" + str(outputFileExt))
    outputName = outputFileName + outputFileExt
    while not findName :
        if not os.path.exists(outputName):
            findName = True
        else :
            outputName = outputFileName + "_" + str(i) + outputFileExt
            i += 1

    cmd='MP4Box ' + fileListConcat + ' -new "' + outputName + '"'
    log.info(HEADER, "In  concatFile cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()
    if (procPopen.returncode != 0) :
        errC += 1
        log.error(HEADER, "In  concatFile file: issue with " + str(cmd))

    log.info(HEADER, "Out concatFile")

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
    firstN = str()
    outputN = str()
    log.info(HEADER, "In  main")

    fileList = list()
    fileListConvert = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".mp4", ".MP4", ".avi", ".AVI"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        log.exit("Convert X MP4 to 1 MP4", "No video has been found\n")

    ## Concat them
    log.info(HEADER, "fileList="+str(fileList))
    concatFile(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Concat videos", "\nJob fini.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


