#!/usr/bin/env python
# -*- coding: latin1 -*-

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

        if (fileD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out convertFile")


#def convertFile(fileL, fileDest) :
#    global dbg
#    global errC
#    dbg.info(HEADER, "In  convertFile")
#
#    cmd='convert ' + fileL + ' ' + fileDest + '.pdf'
#    dbg.info(HEADER, "In  convertFile cmd=" + str(cmd))
#    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
#    procPopen.wait()
#    if (procPopen.returncode != 0) :
#        errC += 1
#        dbg.error(HEADER, "In  convertFile file: issue with " + str(cmd))
#
#    dbg.info(HEADER, "Out convertFile")
#
#
#
#def changeAndConvert(fileD, fileL, fileDest) :
#    global dbg
#    global errC
#    dbg.info(HEADER, "In  changeAndConvert")
#
#    oldDir = os.getcwd()
#
#    if (fileD != "") :
#        os.chdir(fileD)
#    convertFile(fileL, fileDest)
#    if (fileD != "") :
#        os.chdir(oldDir)
#
#    dbg.info(HEADER, "Out changeAndConvert")
#
#
#
#def convertFiles(fileList) :
#    global dbg
#    global errC
#    dbg.info(HEADER, "In  convertFiles")
#
#    fileL_str = str()
#    fileD_mem = "unknown_directory"
#    fileDest = str()
#
#    for (fileD, fileN, fileE) in fileList :
#        dbg.debug("fileD=" + fileD + ", fileN=" + fileN + ", fileE=" + fileE)
#        if (fileD_mem != fileD) :
#            dbg.debug("fileD_mem=" + fileD_mem + ", fileD=" + fileD)
#            if (fileD_mem == "unknown_directory") :
#                fileD_mem = fileD
#                fileL_str += fileN + fileE + " "
#                fileDest = fileN
#                dbg.debug("1 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#            else :
#                dbg.debug("5 fileL_str=" + fileL_str + ", fileDest=" + fileDest)
#                changeAndConvert(fileD, fileL_str, fileDest)
#
#                fileD_mem = fileD
#                fileL_str = fileN + fileE + " "
#                fileDest = fileN
#                dbg.debug("2 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#        else :
#            fileD_mem = fileD
#            fileL_str += fileN + fileE + " "
#            dbg.debug("3 fileD_mem=" + fileD_mem + ", fileL_str=" + fileL_str)
#
#    changeAndConvert(fileD, fileL_str, fileDest)
#
#    dbg.info(HEADER, "Out convertFiles")

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
    extAuth=[".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        dbg.exit("Convert JPG to PDF", "No image has been found\n")

    ## Convert them
    dbg.debug("fileList="+str(fileList))
    convertFile(fileList)

    ## End dialog
    dialog_end(warnC, errC, logFile, "Convert images", "\nJob fini.")
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)
    main()


