#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Split flac file into several thanks to cue file
'''



## Import
import sys
import os
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "SpliFlac"

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
fileFlac = str()

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def splitFlac(fileList) :
    global dbg
    global errC
    global fileFlac
    dbg.info(HEADER, "In  splitFlac")

    oldDir = os.getcwd()

    (file1D, file1N, file1E) = fileList[0]
    (file2D, file2N, file2E) = fileList[1]
    dbg.info(HEADER, "In  splitFlac file1=" + os.path.join(file1D, file1N + file1E))
    dbg.info(HEADER, "In  splitFlac file2=" + os.path.join(file2D, file2N + file2E))

    if ( (file1E == ".cue") or (file1E == ".CUE") ) and ((file2E == ".flac") or (file2E == ".FLAC") ) :
        fileCueD = file1D
        fileCueN = file1N
        fileCueE = file1E
        fileFlacD = file2D
        fileFlacN = file2N
        fileFlacE = file2E
    elif ( (file2E == ".cue") or (file2E == ".CUE") ) and ((file1E == ".flac") or (file1E == ".FLAC") ) :
        fileCueD = file2D
        fileCueN = file2N
        fileCueE = file2E
        fileFlacD = file1D
        fileFlacN = file1N
        fileFlacE = file1E
    else :
        dialog_error("Split Flac with Cue", "\nThe 2 files must be flac AND cue.\n")

    dbg.info(HEADER, "In  splitFlac fileCue=" + os.path.join(fileCueD, fileCueN + fileCueE))
    dbg.info(HEADER, "In  splitFlac fileFlac=" + os.path.join(fileFlacD, fileFlacN + fileFlacE))
    fileFlac = os.path.join(fileFlacD, fileFlacN + fileFlacE)

    if (fileFlacD != fileCueD) :
        dialog_error("Split Flac with Cue", "\nThe 2 files flac and cue mus be in the same directory.\n")

    if (fileFlacD != "") :
        os.chdir(fileFlacD)

    cmd='shntool split -t "%p - %a - %n - %t" -f "' + fileCueN + fileCueE + '" -o flac "' + fileFlacN + fileFlacE + '"'
    dbg.info(HEADER, "In  splitFlac cmd=" + str(cmd))
    procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
    dbg.info(HEADER, "In  splitFlac before wait")
    procPopen.wait()
    dbg.info(HEADER, "In  splitFlac after wait returnCode = " + str(procPopen.returncode))
    if (procPopen.returncode != 0) :
        errC += 1
        dbg.error(HEADER, "In  splitFlac file: issue with " + str(os.path.join(fileFlacD, fileFlacN + fileFlacE)))

    dbg.info(HEADER, "In  splitFlac after check")
    if (fileFlacD != "") :
        os.chdir(oldDir)

    dbg.info(HEADER, "Out splitFlac")

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
    extAuth=[".flac", ".FLAC", ".cue", ".CUE"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        dialog_error("Split Flac with Cue", "\nNo flac and cue file have been found\n")
    elif (len(fileList) != 2) :
        dialog_error("Split Flac with Cue", "\nOnly 2 files are allowed = flac and cue\n")

    dbg.info(HEADER, "In  main filelist = " + str(len(fileList)))

    ## Split it
    splitFlac(fileList)

    ## End dialog
    dialog_end(warnC, errC, logFile, "Convert images", "\nJob fini : " + str(fileFlac) + " splitted.")
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()


