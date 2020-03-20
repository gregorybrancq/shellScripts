#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Convert X jpg to 1 pdf
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "XJpgTO1Pdf"

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

def convertFile(fileList) :
    global log
    global errC
    fileListConvert = list()

    log.info(HEADER, "In  convertFile")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        log.info(HEADER, "In  convertFile directory " + str(fileD) + "  convertFile " + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='convert "' + fileN + fileE + '" "' + fileN + '.pdf"'
        log.info(HEADER, "In  convertFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            log.error(HEADER, "In  convertFile file: issue with " + str(os.path.join(fileD, fileN + fileE)))
        else :
            fileListConvert.append([fileD, fileN, ".pdf"])

        if (fileD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out convertFile")
    return fileListConvert



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
    return (firstFileName, outputName)



def cleanFiles(fileList, firstN, outputN) :
    global log
    global errC
    log.info(HEADER, "In  cleanFiles")

    for (fileD, fileN, fileE) in fileList :
        if os.path.exists(os.path.join(fileD, fileN + fileE)):
            os.remove(os.path.join(fileD, fileN + fileE))

    if os.path.exists(outputN) :
        os.rename(outputN, firstN + ".pdf")

    log.info(HEADER, "Out cleanFiles")

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
    extAuth=[".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        log.exit("Convert X JPG to 1 PDF", "No image has been found\n")

    ## Convert them
    log.dbg("fileList="+str(fileList))
    fileListConvert = convertFile(fileList)

    ## Concat them
    log.dbg("fileListConvert="+str(fileListConvert))
    (firstN, outputN) = concatFile(fileListConvert)

    ## Delete intermediary files
    log.dbg("fileListConvert="+str(fileListConvert))
    cleanFiles(fileListConvert, firstN, outputN)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Convert images", "\nJob fini.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()


