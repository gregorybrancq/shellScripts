#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Concatenate PDF files
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "XPdfTO1Pdf"

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

    fileListStr = ""
    firstFileName = ""
    for (fileD, fileN, fileE) in fileList :
        if (firstFileName == "") :
            firstFileName = fileN
        if (fileD != "") :
            fileListStr += fileD + "/"

        fileListStr += '"' + fileN + fileE + '" '

    findName = False
    i = 0
    outputName = firstFileName + ".pdf"
    while not findName :
        if not os.path.exists(outputName):
            findName = True
        else :
            outputName = firstFileName + "_" + str(i) + ".pdf"
            i += 1

    cmd='pdftk ' + fileListStr + ' cat output "' + outputName + '"'
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
    log.info(HEADER, "In  main")

    fileList = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".pdf", ".PDF"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one pdf file
    if (len(fileList) == 0) :
        log.exit("1", "No pdf file found\n")

    ## Convert them
    log.dbg("fileList="+str(fileList))
    concatFile(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Concat PDF files", "\nJob fini.")

    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


