#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Reduce the weight of the pdf files
'''



## Import
import sys
import os
import shutil
from datetime import datetime
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

def reduceWeight(fileList) :
    global log
    global errC
    log.info(HEADER, "In  reduceWeight")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        log.info(HEADER, "In  reduceWeight directory=" + str(fileD) + ", file=" + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="' + fileN + ' reduced' + fileE + '" "' + fileN + fileE + '"'
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            log.error(HEADER, "In  reduceWeight file: issue with " + str(os.path.join(fileD, fileN + fileE)))
        else :
            # is it worth to move the result?
            originalSize = os.path.getsize(fileN + fileE)
            reducedSize = os.path.getsize(fileN + ' reduced' + fileE)

            if (originalSize - reducedSize > 0) :
                # move file
                if os.path.exists(fileN + fileE):
                    os.remove(fileN + fileE)
                shutil.move(fileN + ' reduced' + fileE, fileN + fileE)
                log.info(HEADER, "In  reduceWeight copied file. Gain = " + str(humanSize(originalSize - reducedSize)) + ", original = " + str(humanSize(originalSize)) + ", reduced = " + str(humanSize(reducedSize)))
            else :
                # remove result file
                if os.path.exists(fileN + ' reduced' + fileE):
                    os.remove(fileN + ' reduced' + fileE)
                log.info(HEADER, "In  reduceWeight removed file. Original = " + str(humanSize(originalSize)) + ", reduced = " + str(humanSize(reducedSize)))

        if (fileD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out reduceWeight")

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

    ## Verify if there is at least one photo to reducePdfWeight
    if (len(fileList) == 0) :
        MessageDialog(type_='error', title="Reduce PDF weight", message="\nNo pdf file has been found\n").run()
    else :
        log.info(HEADER, "In  main reduce pdf weight = " + str(len(fileList)))

    ## Convert them
    reduceWeight(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Reduce PDF weight", "\nJob fini : " + str(len(fileList)) + " pdf reduced.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


