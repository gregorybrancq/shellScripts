#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Reduce the weight of the pdf files
'''



## Import
import sys
import os
import shutil
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "Reduce_Pdf_Weight"

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

def reduceWeight(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  reduceWeight")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        dbg.info(HEADER, "In  reduceWeight directory=" + str(fileD) + ", file=" + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="' + fileN + ' reduced' + fileE + '" "' + fileN + fileE + '"'
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            dbg.error(HEADER, "In  reduceWeight file: issue with " + str(os.path.join(fileD, fileN + fileE)))
        else :
            # is it worth to move the result?
            originalSize = os.path.getsize(fileN + fileE)
            reducedSize = os.path.getsize(fileN + ' reduced' + fileE)

            if (originalSize - reducedSize > 0) :
                # move file
                if os.path.exists(fileN + fileE):
                    os.remove(fileN + fileE)
                shutil.move(fileN + ' reduced' + fileE, fileN + fileE)
                dbg.info(HEADER, "In  reduceWeight copied file. Gain = " + str(humanSize(originalSize - reducedSize)) + ", original = " + str(humanSize(originalSize)) + ", reduced = " + str(humanSize(reducedSize)))
            else :
                # remove result file
                if os.path.exists(fileN + ' reduced' + fileE):
                    os.remove(fileN + ' reduced' + fileE)
                dbg.info(HEADER, "In  reduceWeight removed file. Original = " + str(humanSize(originalSize)) + ", reduced = " + str(humanSize(reducedSize)))

        if (fileD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out reduceWeight")

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

    ## Verify if there is at least one photo to reducePdfWeight
    if (len(fileList) == 0) :
        dialog_error("Reduce PDF weight", "\nNo pdf file has been found\n")
    else :
        dbg.info(HEADER, "In  main reduce pdf weight = " + str(len(fileList)))

    ## Convert them
    reduceWeight(fileList)

    msg = "\nJob fini : " + str(len(fileList)) + " pdf reduced.\n"
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    if (errC != 0) :
        msg += "\nError = " + str(errC)
    msg += "\n\nLog file = " + str(logFile)
    dialog_info("Reduce PDF weight", msg)
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


