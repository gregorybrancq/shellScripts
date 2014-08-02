#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Convert X jpg to 1 pdf
'''



## Import
import sys
import os
import time, datetime
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

def convertFile(fileList) :
    global dbg
    global errC
    fileListConvert = list()

    dbg.info(HEADER, "In  convertFile")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        dbg.info(HEADER, "In  convertFile directory " + str(fileD) + "  convertFile " + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='convert "' + fileN + fileE + '" "' + fileN + '.pdf"'
        dbg.info(HEADER, "In  convertFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            dbg.error(HEADER, "In  convertFile file: issue with " + str(os.path.join(fileD, fileN + fileE)))
        else :
            fileListConvert.append([fileD, fileN, ".pdf"])

        if (fileD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out convertFile")
    return fileListConvert



def concatFile(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  concatFile")

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

    cmd='pdftk ' + fileListStr + ' cat output ' + outputName
    dbg.info(HEADER, "In  concatFile cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    procPopen.wait()
    if (procPopen.returncode != 0) :
        errC += 1
        dbg.error(HEADER, "In  concatFile file: issue with " + str(cmd))

    dbg.info(HEADER, "Out concatFile")
    return (firstFileName, outputName)



def cleanFiles(fileList, firstN, outputN) :
    global dbg
    global errC
    dbg.info(HEADER, "In  cleanFiles")

    for (fileD, fileN, fileE) in fileList :
        if os.path.exists(os.path.join(fileD, fileN + fileE)):
            os.remove(os.path.join(fileD, fileN + fileE))

    if os.path.exists(outputN) :
        os.rename(outputN, firstN + ".pdf")

    dbg.info(HEADER, "Out cleanFiles")

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
    firstN = str()
    outputN = str()
    dbg.info(HEADER, "In  main")

    fileList = list()
    fileListConvert = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".jpg", ".JPG", ".tif", ".TIF", ".gif", ".GIF"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one photo to convertPdf2Jpg
    if (len(fileList) == 0) :
        dbg.exit("1", "No image has been found\n")

    ## Convert them
    dbg.debug("fileList="+str(fileList))
    fileListConvert = convertFile(fileList)

    ## Concat them
    dbg.debug("fileListConvert="+str(fileListConvert))
    (firstN, outputN) = concatFile(fileListConvert)

    ## Delete intermediary files
    dbg.debug("fileListConvert="+str(fileListConvert))
    cleanFiles(fileListConvert, firstN, outputN)

    msg = "\nJob fini.\n"
    dbg.debug("11")
    if (warnC != 0) :
        dbg.debug("12")
        msg += "\nWarning = " + str(warnC)
    dbg.debug("13")
    if (errC != 0) :
        dbg.debug("14")
        msg += "\nError = " + str(errC)
    dbg.debug("15")
    msg += "\n\nLog file = " + str(logFile)
    dbg.debug("16 msg=" + str(msg))
    dialog_info("Convert images", msg)
    dbg.debug("17")
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


