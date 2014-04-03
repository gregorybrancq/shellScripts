#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Concatene PDF files
'''



## Import
import sys
import os
import time, datetime
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

def concatFile(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  concatFile")

    fileListStr = ""
    for (fileD, fileN, fileE) in fileList :
        if (fileD != "") :
            fileListStr += fileD + "/"

        fileListStr += fileN + fileE + " "

    findName = False
    outputName = "concat.pdf"
    i = 0
    while not findName :
        if not os.path.exists(outputName):
            findName = True
        else :
            outputName = "concat_" + str(i) + ".pdf"
            i += 1

    cmd='pdftk ' + fileListStr + ' cat output ' + outputName
    dbg.info(HEADER, "In  concatFile cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()
    if (procPopen.returncode != 0) :
        errC += 1
        dbg.error(HEADER, "In  concatFile file: issue with " + str(cmd))

    dbg.info(HEADER, "Out concatFile")

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

    fileList = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".pdf", ".PDF"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one pdf file
    if (len(fileList) == 0) :
        dbg.exit("1", "No pdf file found\n")

    ## Convert them
    dbg.debug("fileList="+str(fileList))
    concatFile(fileList)

    msg = "\nJob fini.\n"
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    if (errC != 0) :
        msg += "\nError = " + str(errC)
    msg += "\n\nLog file = " + str(logFile)
    dialog_info("Concat PDF files", msg)
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


