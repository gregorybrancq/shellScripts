#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Convert jpg to pdf
'''



## Import
import sys
import os
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "JpgTOPdf"

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
    global log
    global errC
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

        if (fileD != "") :
            os.chdir(oldDir)

    log.info(HEADER, "Out convertFile")


#def convertFile(fileL, fileDest) :
#    global log
#    global errC
#    log.info(HEADER, "In  convertFile")
#
#    cmd='convert ' + fileL + ' ' + fileDest + '.pdf'
#    log.info(HEADER, "In  convertFile cmd=" + str(cmd))
#    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
#    procPopen.wait()
#    if (procPopen.returncode != 0) :
#        errC += 1
#        log.error(HEADER, "In  convertFile file: issue with " + str(cmd))
#
#    log.info(HEADER, "Out convertFile")
#
#
#
#def changeAndConvert(fileD, fileL, fileDest) :
#    global log
#    global errC
#    log.info(HEADER, "In  changeAndConvert")
#
#    oldDir = os.getcwd()
#
#    if (fileD != "") :
#        os.chdir(fileD)
#    convertFile(fileL, fileDest)
#    if (fileD != "") :
#        os.chdir(oldDir)
#
#    log.info(HEADER, "Out changeAndConvert")
#
#
#
#def convertFiles(fileList) :
#    global log
#    global errC
#    log.info(HEADER, "In  convertFiles")
#
#    fileL_str = str()
#    fileD_mem = "unknown_directory"
#    fileDest = str()
#
#    for (fileD, fileN, fileE) in fileList :
#        log.dbg("fileD=" + fileD + ", fileN=" + fileN + ", fileE=" + fileE)
#        if (fileD_mem != fileD) :
#            log.dbg("fileD_mem=" + fileD_mem + ", fileD=" + fileD)
#            if (fileD_mem == "unknown_directory") :
#                fileD_mem = fileD
#                fileL_str += fileN + fileE + " "
#                fileDest = fileN
#                log.dbg("1 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#            else :
#                log.dbg("5 fileL_str=" + fileL_str + ", fileDest=" + fileDest)
#                changeAndConvert(fileD, fileL_str, fileDest)
#
#                fileD_mem = fileD
#                fileL_str = fileN + fileE + " "
#                fileDest = fileN
#                log.dbg("2 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#        else :
#            fileD_mem = fileD
#            fileL_str += fileN + fileE + " "
#            log.dbg("3 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#
#    changeAndConvert(fileD, fileL_str, fileDest)
#
#    log.info(HEADER, "Out convertFiles")

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
    extAuth=[".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        log.exit("Convert JPG to PDF", "No image has been found\n")

    ## Convert them
    log.dbg("fileList="+str(fileList))
    convertFile(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Convert images", "\nJob fini.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)
    main()


