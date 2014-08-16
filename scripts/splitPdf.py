#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Split PDF files
'''



## Import
import sys
import os
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "1PdfTOXPdf"

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

def splitFile(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  splitFile")

    fileListStr = ""
    for (fileD, fileN, fileE) in fileList :
        if (fileD != "") :
            fileListStr += fileD + "/"

        fileListStr += '"' + fileN + fileE + '" '

    findName = False
    outputName = "concat.pdf"
    i = 0
    while not findName :
        if not os.path.exists(outputName):
            findName = True
        else :
            outputName = "concat_" + str(i) + ".pdf"
            i += 1

    cmd='pdftk ' + fileListStr + ' burst'
    dbg.info(HEADER, "In  splitFile cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()
    if (procPopen.returncode != 0) :
        errC += 1
        dbg.error(HEADER, "In  splitFile file: issue with " + str(cmd))

    dbg.info(HEADER, "Out splitFile")

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
    splitFile(fileList)

    ## End dialog
    dialog_end(warnC, errC, logFile, "Split PDF files", "\nJob fini.")
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


